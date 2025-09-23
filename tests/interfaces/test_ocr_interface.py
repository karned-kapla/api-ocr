import pytest
from typing import List, Dict, Any

from interfaces.ocr_interface import OcrRepository
from models.ocr_model import OcrWrite


class TestOcrRepository(OcrRepository):
    """
    A concrete implementation of the OcrRepository interface for testing.
    """
    def __init__(self):
        self.ocrs = {}
        self.is_closed = False

    def create_ocr(self, ocr_create: OcrWrite) -> str:
        ocr_id = "test-uuid"
        self.ocrs[ocr_id] = ocr_create
        return ocr_id

    def get_ocr(self, ocr_id: str) -> Dict[str, Any]:
        if ocr_id in self.ocrs:
            return {"uuid": ocr_id, "name": self.ocrs[ocr_id].name}
        return None

    def list_ocrs(self) -> List[Dict[str, Any]]:
        return [{"uuid": ocr_id, "name": ocr.name} for ocr_id, ocr in self.ocrs.items()]

    def update_ocr(self, ocr_id: str, ocr_update: OcrWrite) -> None:
        if ocr_id in self.ocrs:
            self.ocrs[ocr_id] = ocr_update

    def delete_ocr(self, ocr_id: str) -> None:
        if ocr_id in self.ocrs:
            del self.ocrs[ocr_id]

    def close(self) -> None:
        self.is_closed = True


def test_ocr_repository_interface():
    """
    Test that a concrete implementation of OcrRepository can be created
    and that it implements all the required methods.
    """
    # Create a concrete implementation
    repo = TestOcrRepository()

    # Test create_ocr
    ocr = OcrWrite(name="Test Ocr")
    ocr_id = repo.create_ocr(ocr)
    assert ocr_id == "test-uuid"

    # Test get_ocr
    retrieved_ocr = repo.get_ocr(ocr_id)
    assert retrieved_ocr["uuid"] == ocr_id
    assert retrieved_ocr["name"] == "Test Ocr"

    # Test list_ocrs
    ocrs = repo.list_ocrs()
    assert len(ocrs) == 1
    assert ocrs[0]["uuid"] == ocr_id
    assert ocrs[0]["name"] == "Test Ocr"

    # Test update_ocr
    updated_ocr = OcrWrite(name="Updated Ocr")
    repo.update_ocr(ocr_id, updated_ocr)
    retrieved_ocr = repo.get_ocr(ocr_id)
    assert retrieved_ocr["name"] == "Updated Ocr"

    # Test delete_ocr
    repo.delete_ocr(ocr_id)
    assert repo.get_ocr(ocr_id) is None

    # Test close
    repo.close()
    assert repo.is_closed


def test_ocr_repository_abstract_methods():
    """
    Test that OcrRepository cannot be instantiated directly
    because it has abstract methods.
    """
    with pytest.raises(TypeError) as exc:
        OcrRepository()

    assert "Can't instantiate abstract class OcrRepository" in str(exc.value)
    assert "abstract methods" in str(exc.value)