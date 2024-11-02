from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()
FHIR_API_URL = "http://localhost:32783/fhir/r4/Patient"

@app.get("/patient/{patient_id}")
async def get_patient(patient_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FHIR_API_URL}/{patient_id}")
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Patient not found")

@app.get("/patient")
async def get_all_patients():
    async with httpx.AsyncClient() as client:
        response = await client.get(FHIR_API_URL)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error retrieving patients")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)