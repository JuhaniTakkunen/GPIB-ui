from fastapi import FastAPI, HTTPException
from fastapi_cors import CORS
from pydantic import BaseModel, validator, field_validator
import visa
import visa.error
from gpib_interface.control import GpibController

app = FastAPI()
# Add CORS middleware
origins = ["*"]  # Replace with the actual allowed origins (e.g., "http://localhost:3000") for production
app.add_middleware(
    CORS,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models for API requests
class RangeRequest(BaseModel):
    start_wl: float
    stop_wl: float

class ReferenceRequest(BaseModel):
    reference: float

class ResolutionRequest(BaseModel):
    resolution: float

class ActiveTraceRequest(BaseModel):
    trace: str

    @field_validator('trace')
    @classmethod
    def validate_trace(cls, value):
        value = value.upper()
        accepted_values = {"A", "B", "C"}
        if value not in accepted_values:
            raise ValueError(f"Trace must be one of: {accepted_values}")
        return value


@app.get("/health")
async def health_check():
    """
    Check if the connection to the GPIB device is healthy.
    """
    with GpibController() as controller:
        try:
            controller.status()
            return {"status": "OK"}
        except visa.error.VISAError:
            raise HTTPException(status_code=500, detail="Communication with GPIB device failed.")

@app.post("/range")
async def set_range(request: RangeRequest):
    """
    Set the wavelength range for the measurement [nm].
    """
    with GpibController() as controller:
        controller.handle_range(request.start_wl, request.stop_wl)
        return {"message": "Range set successfully."}

@app.post("/reference")
async def set_reference(request: ReferenceRequest):
    """
    Set reference level (-90.0 to 20.0 dBm)
    """
    with GpibController() as controller:
        controller.handle_ref(request.reference)
        return {"message": "Range set successfully."}

@app.post("/resolution")
async def set_resolution(request: ResolutionRequest):
    """
    Set resolution (0.05 to 10 nm)
    """
    with GpibController() as controller:
        controller.handle_res(request.resolution)
        return {"message": "Range set successfully."}

@app.post("/active_trace")
async def set_active_trace(active_trace_request: ActiveTraceRequest):
    """
    Set the active trace.
    """
    with GpibController() as controller:
        controller.handle_active(active_trace_request.trace)
        return {"message": "Active trace set successfully."}

# ... other endpoints for other commands ...

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
