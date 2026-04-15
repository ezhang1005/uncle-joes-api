from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import bigquery
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Uncle Joes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PROJECT = "uncle-joes-coffee-company" 
DATASET = "uncle_joes"
FULL_PATH = f"{DATA_PROJECT}.{DATASET}"

def get_bq_client():
    client = bigquery.Client()
    try:
        yield client
    finally:
        client.close()

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Uncle Joe's API is online"}

# --- MENU ENDPOINT ---
@app.get("/menu")
def get_menu(bq: bigquery.Client = Depends(get_bq_client)):
    query = f"SELECT name, price, category FROM `{FULL_PATH}.menu_items` LIMIT 20"
    try:
        query_job = bq.query(query)
        results = [dict(row) for row in query_job]
        return {"items": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BigQuery Error: {str(e)}")
# --- LOCATIONS ENDPOINTS ---
# --- FINAL LOCATIONS CODE ---

@app.get("/locations")
def get_locations(bq: bigquery.Client = Depends(get_bq_client)):
    # Pulling the UUID 'id' and the 'city/state' so the user knows which is which
    query = f"""
        SELECT id, city, state, open_for_business 
        FROM `{FULL_PATH}.locations`
        ORDER BY state, city ASC
    """
    try:
        query_job = bq.query(query)
        results = [dict(row) for row in query_job]
        return {"total": len(results), "locations": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BigQuery Error: {str(e)}")

@app.get("/locations/{location_id}")
def get_store_detail(location_id: str, bq: bigquery.Client = Depends(get_bq_client)):
    # location_id will be that long UUID string
    query = f"SELECT * FROM `{FULL_PATH}.locations` WHERE id = @lid"
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("lid", "STRING", location_id)]
    )
    
    try:
        query_job = bq.query(query, job_config=job_config)
        results = [dict(row) for row in query_job]
        
        if not results:
            raise HTTPException(status_code=404, detail="Store UUID not found")
            
        return results[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BigQuery Error: {str(e)}")