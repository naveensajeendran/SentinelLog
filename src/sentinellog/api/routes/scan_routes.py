from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
from sentinellog.api.services.detection_service import DetectionService

router = APIRouter()

service = DetectionService("src/sentinellog/rules/rules.yaml")


class ScanRequest(BaseModel):
    filepath: str | None = None
    content: str | None = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filepath": None,
                "content": "ERROR [2025-11-27] Failed login attempt from 192.168.1.100"
            }
        }
    )


@router.post("/scan")
def scan(req: ScanRequest):
    """Scan logs for threats.
    
    Accepts either a filepath or inline content.
    Returns list of detected threats with severity levels.
    """
    if not req.filepath and not req.content:
        raise HTTPException(status_code=400, detail="Provide filepath or content")

    try:
        if req.filepath:
            threats = service.scan_file(req.filepath)
        else:
            threats = service.scan_text(req.content)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"File not found: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan error: {str(e)}")

    return {
        "status": "success",
        "count": len(threats),
        "data": [t.__dict__ for t in threats]
    }


@router.post("/rules/reload")
def reload_rules():
    """Reload rules from disk without restarting service."""
    try:
        service.reload_rules()
        return {"status": "success", "message": "Rules reloaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reload error: {str(e)}")


@router.get("/rules/list")
def list_rules():
    """List active detection rules."""
    return {
        "status": "success",
        "count": len(service.list_rules()),
        "rules": service.list_rules()
    }
