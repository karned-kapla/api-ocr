

def ocr_serial(ocr) -> dict:
    return {
        "uuid": str(ocr["_id"]),
        "url": ocr.get("url"),
        "model": ocr.get("model"),
        "status": ocr.get("status"),
        "result": ocr.get("result"),
        "created_by": ocr.get("created_by"),
        "secret": ocr.get("secret")
    }


def list_ocr_serial(ocrs) -> list:
    return [ocr_serial(ocr) for ocr in ocrs]
