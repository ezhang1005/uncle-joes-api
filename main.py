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
@app.get("/locations")
def get_locations(bq: bigquery.Client = Depends(get_bq_client)):
    # Try selecting * first to see all available columns if you're unsure
    query = f"SELECT * FROM `{FULL_PATH}.locations` LIMIT 10"
    try:
        query_job = bq.query(query)
        results = [dict(row) for row in query_job]
        return {"total": len(results), "locations": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BigQuery Error: {str(e)}")

@app.get("/locations/{store_id}")
def get_store_detail(store_id: str, bq: bigquery.Client = Depends(get_bq_client)):
    # Using parameterized query to safely handle the store_id
    query = f"SELECT * FROM `{FULL_PATH}.locations` WHERE store_id = @sid"
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("sid", "STRING", store_id)]
    )
    
    try:
        query_job = bq.query(query, job_config=job_config)
        results = [dict(row) for row in query_job]
        
        if not results:
            raise HTTPException(status_code=404, detail=f"Store ID {store_id} not found")
            
        return results[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BigQuery Error: {str(e)}")