import pytest
from unittest.mock import patch, MagicMock
import re
from uuid import UUID

from repositories.ocr_repository_mongo import check_uri, extract_database, OcrRepositoryMongo
from models.ocr_model import OcrWrite


def test_check_uri_valid():
    # Should not raise an exception
    check_uri("mongodb://localhost:27017/test")


def test_check_uri_invalid():
    with pytest.raises(ValueError) as exc:
        check_uri("invalid://localhost:27017/test")

    assert str(exc.value) == "Invalid URI: URI must start with 'mongodb://'"


def test_extract_database_valid():
    db_name = extract_database("mongodb://localhost:27017/test_db")
    assert db_name == "test_db"


def test_extract_database_no_db():
    with pytest.raises(ValueError) as exc:
        extract_database("mongodb://localhost:27017/")

    assert "L'URI MongoDB ne contient pas de nom de base de données" in str(exc.value)


class TestOcrRepositoryMongo:
    @pytest.fixture
    def mock_mongo_client(self):
        with patch('repositories.ocr_repository.MongoClient') as mock_client:
            # Create a mock MongoDB client
            client_instance = MagicMock()
            mock_client.return_value = client_instance

            # Create a mock database
            db_instance = MagicMock()
            client_instance.__getitem__.return_value = db_instance

            # Create a mock collection
            collection_instance = MagicMock()
            db_instance.__getitem__.return_value = collection_instance

            yield mock_client, client_instance, db_instance, collection_instance

    def test_init(self, mock_mongo_client):
        mock_client, client_instance, db_instance, _ = mock_mongo_client

        # Initialize the repository
        repo = OcrRepositoryMongo("mongodb://localhost:27017/test_db")

        # Verify the client was created with the correct URI
        mock_client.assert_called_once_with("mongodb://localhost:27017/test_db")

        # Verify the database was accessed
        client_instance.__getitem__.assert_called_once_with("test_db")

        # Verify the repository properties
        assert repo.uri == "mongodb://localhost:27017/test_db"
        assert repo.client == client_instance
        assert repo.db == db_instance
        assert repo.collection == "ocrs"

    def test_create_ocr(self, mock_mongo_client):
        _, _, _, collection_instance = mock_mongo_client

        # Mock the insert_one method
        insert_result = MagicMock()
        insert_result.inserted_id = "test-uuid"
        collection_instance.insert_one.return_value = insert_result

        # Create a test ocr
        ocr = OcrWrite(name="Test Ocr")

        # Initialize the repository and create the ocr
        repo = OcrRepositoryMongo("mongodb://localhost:27017/test_db")
        result = repo.create_ocr(ocr)

        # Verify the result
        assert result == "test-uuid"

        # Verify insert_one was called with the correct data
        call_args = collection_instance.insert_one.call_args[0][0]
        assert call_args["name"] == "Test Ocr"
        assert "_id" in call_args
        # Verify the _id is a valid UUID
        assert re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', call_args["_id"])

    def test_create_ocr_error(self, mock_mongo_client):
        _, _, _, collection_instance = mock_mongo_client

        # Mock the insert_one method to raise an exception
        collection_instance.insert_one.side_effect = Exception("Database connection error")

        # Create a test ocr
        ocr = OcrWrite(name="Test Ocr")

        # Initialize the repository
        repo = OcrRepositoryMongo("mongodb://localhost:27017/test_db")

        # Verify that the method raises a ValueError with the expected message
        with pytest.raises(ValueError) as exc:
            repo.create_ocr(ocr)

        # Check that the error message contains the original exception message
        assert "Failed to create ocr in database" in str(exc.value)
        assert "Database connection error" in str(exc.value)

    def test_get_ocr(self, mock_mongo_client):
        _, _, _, collection_instance = mock_mongo_client

        # Mock the find_one method
        collection_instance.find_one.return_value = {
            "_id": "test-uuid",
            "name": "Test Ocr",
            "description": "Test Description"
        }

        # Initialize the repository and get the ocr
        repo = OcrRepositoryMongo("mongodb://localhost:27017/test_db")

        # Mock the ocr_serial function
        with patch('repositories.ocr_repository.ocr_serial', return_value={"uuid": "test-uuid", "name": "Test Ocr"}):
            result = repo.get_ocr("test-uuid")

        # Verify the result
        assert result == {"uuid": "test-uuid", "name": "Test Ocr"}

        # Verify find_one was called with the correct query
        collection_instance.find_one.assert_called_once_with({"_id": "test-uuid"})

    def test_list_ocrs(self, mock_mongo_client):
        _, _, _, collection_instance = mock_mongo_client

        # Mock the find method
        mock_cursor = MagicMock()
        collection_instance.find.return_value = mock_cursor

        # Initialize the repository and list the ocrs
        repo = OcrRepositoryMongo("mongodb://localhost:27017/test_db")

        # Mock the list_ocr_serial function
        with patch('repositories.ocr_repository.list_ocr_serial', return_value=[{"uuid": "test-uuid", "name": "Test Ocr"}]):
            result = repo.list_ocrs()

        # Verify the result
        assert result == [{"uuid": "test-uuid", "name": "Test Ocr"}]

        # Verify find was called
        collection_instance.find.assert_called_once()

    def test_update_ocr(self, mock_mongo_client):
        _, _, _, collection_instance = mock_mongo_client

        # Initialize the repository and update the ocr
        repo = OcrRepositoryMongo("mongodb://localhost:27017/test_db")
        ocr = OcrWrite(name="Updated Ocr")
        repo.update_ocr("test-uuid", ocr)

        # Verify find_one_and_update was called with the correct arguments
        collection_instance.find_one_and_update.assert_called_once()
        args, _ = collection_instance.find_one_and_update.call_args
        assert args[0] == {"_id": "test-uuid"}
        assert "$set" in args[1]
        assert args[1]["$set"]["name"] == "Updated Ocr"

    def test_delete_ocr(self, mock_mongo_client):
        _, _, _, collection_instance = mock_mongo_client

        # Initialize the repository and delete the ocr
        repo = OcrRepositoryMongo("mongodb://localhost:27017/test_db")
        repo.delete_ocr("test-uuid")

        # Verify delete_one was called with the correct query
        collection_instance.delete_one.assert_called_once_with({"_id": "test-uuid"})

    def test_close(self, mock_mongo_client):
        _, client_instance, _, _ = mock_mongo_client

        # Initialize the repository and close it
        repo = OcrRepositoryMongo("mongodb://localhost:27017/test_db")
        repo.close()

        # Verify close was called
        client_instance.close.assert_called_once()

    def test_context_manager(self, mock_mongo_client):
        _, client_instance, _, _ = mock_mongo_client

        # Initialize the repository
        repo = OcrRepositoryMongo("mongodb://localhost:27017/test_db")

        # Call __exit__ directly (simulating context manager exit)
        repo.__exit__(None, None, None)

        # Verify close was called
        client_instance.close.assert_called_once()
