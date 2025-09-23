import pytest
from pydantic import ValidationError

from models.ocr_model import OcrWrite


def test_ocr_creation():
    ocr_data = {
        "name": "Ocr Name",
        "description": "This is a ocr description.",
        "price": 10.99,
        "quantity": 2,
        "number_of_persons": 4,
        "origin_country": "France",
        "attributes": ["vegan", "gluten-free"],
        "utensils": ["pan", "knife"],
        "ingredients": [
            {"name": "Sugar", "quantity": 100, "unit": "grams"},
            {"name": "Salt"}
        ],
        "steps": [
            {"step_number": 1, "description": "First step", "duration": "10 min"},
            {"step_number": 2, "description": "Second step"}
        ],
        "thumbnail_url": "http://example.com/thumbnail.jpg",
        "large_image_url": "http://example.com/large_image.jpg",
        "source_reference": "Source Reference"
    }
    ocr = OcrWrite(**ocr_data)
    assert ocr.name == "Ocr Name"
    assert ocr.description == "This is a ocr description."
    assert ocr.price == 10.99
    assert ocr.quantity == 2
    assert ocr.number_of_persons == 4
    assert ocr.origin_country == "France"
    assert ocr.attributes == ["vegan", "gluten-free"]
    assert ocr.utensils == ["pan", "knife"]
    assert len(ocr.ingredients) == 2
    assert len(ocr.steps) == 2
    assert str(ocr.thumbnail_url) == "http://example.com/thumbnail.jpg"
    assert str(ocr.large_image_url) == "http://example.com/large_image.jpg"
    assert ocr.source_reference == "Source Reference"


def test_ocr_creation_with_defaults():
    ocr_data = {
        "name": "Minimal Ocr"
    }
    ocr = OcrWrite(**ocr_data)
    assert ocr.name == "Minimal Ocr"
    assert ocr.description is None
    assert ocr.price is None
    assert ocr.quantity is None
    assert ocr.number_of_persons is None
    assert ocr.origin_country is None
    assert ocr.attributes == []
    assert ocr.utensils == []
    assert ocr.ingredients == []
    assert ocr.steps == []
    assert ocr.thumbnail_url is None
    assert ocr.large_image_url is None
    assert ocr.source_reference is None


def test_ocr_validation_error():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "number_of_persons": 0
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)


def test_ocr_missing_fields():
    incomplete_ocr_data = {
        "description": "Incomplete Ocr"
    }
    with pytest.raises(ValidationError):
        OcrWrite(**incomplete_ocr_data)

def test_ocr_invalid_description_type():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "description": 123
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)

def test_ocr_invalid_price_type():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "price": "ten"
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)

def test_ocr_invalid_quantity_type():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "quantity": "two"
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)

def test_ocr_invalid_number_of_persons_type():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "number_of_persons": "four"
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)

def test_ocr_invalid_origin_country_type():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "origin_country": 42
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)

def test_ocr_invalid_attributes_type():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "attributes": "vegan"
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)

def test_ocr_invalid_utensils_type():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "utensils": "pan"
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)

def test_ocr_invalid_ingredients_type():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "ingredients": "Sugar"
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)

def test_ocr_invalid_steps_type():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "steps": "First step"
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)

def test_ocr_invalid_thumbnail_url_type():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "thumbnail_url": 123
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)

def test_ocr_invalid_large_image_url_type():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "large_image_url": 123
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)

def test_ocr_invalid_source_reference_type():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "source_reference": 123
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)

def test_ocr_invalid_url():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "thumbnail_url": "invalid_url",
        "large_image_url": "invalid_url"
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)

def test_ocr_invalid_list_types():
    invalid_ocr_data = {
        "name": "Invalid Ocr",
        "attributes": ["vegan", 123],
        "utensils": ["pan", 42]
    }
    with pytest.raises(ValidationError):
        OcrWrite(**invalid_ocr_data)