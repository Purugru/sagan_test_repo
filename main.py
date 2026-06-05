from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, Optional
import os
import sqlite3

app = FastAPI()

# Mount templates
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup_event():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            inflow_amount REAL,
            outflow_amount REAL,
            insurance_deductibles REAL
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM clients')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO clients (client_name, inflow_amount, outflow_amount, insurance_deductibles)
            VALUES (?, ?, ?, ?)
        ''', [
            ('John & Jane Doe', 15000, 11000, 2000),
            ('The Smith Family', 22000, 16000, 1500)
        ])
    conn.commit()
    conn.close()

class ReportRequest(BaseModel):
    client_name: str
    inflow_amount: float
    outflow_amount: float
    insurance_deductibles: float
    trust_value: float
    retirement_client_1: Dict[str, float]
    retirement_client_2: Dict[str, float]
    non_retirement: Dict[str, float]
    liabilities: Dict[str, float]

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/generate")
async def generate_report(request: Request, data: ReportRequest):
    # Deterministic Math Formulas
    sacs_excess = data.inflow_amount - data.outflow_amount
    private_reserve_target = (6 * data.outflow_amount) + data.insurance_deductibles
    
    tcc_client_1_retirement_total = sum(data.retirement_client_1.values())
    tcc_client_2_retirement_total = sum(data.retirement_client_2.values())
    tcc_non_retirement_total = sum(data.non_retirement.values())
    
    # Liabilities are NOT subtracted
    tcc_grand_total_net_worth = (
        tcc_client_1_retirement_total + 
        tcc_client_2_retirement_total + 
        tcc_non_retirement_total + 
        data.trust_value
    )
    
    tcc_liabilities_total = sum(data.liabilities.values())

    template_data = {
        "request": request,
        "client_name": data.client_name,
        "inflow_amount": data.inflow_amount,
        "outflow_amount": data.outflow_amount,
        "sacs_excess": sacs_excess,
        "private_reserve_target": private_reserve_target,
        
        "tcc_client_1_retirement_total": tcc_client_1_retirement_total,
        "tcc_client_2_retirement_total": tcc_client_2_retirement_total,
        "tcc_non_retirement_total": tcc_non_retirement_total,
        "trust_value": data.trust_value,
        "tcc_grand_total_net_worth": tcc_grand_total_net_worth,
        "tcc_liabilities_total": tcc_liabilities_total,
        
        "retirement_client_1": data.retirement_client_1,
        "retirement_client_2": data.retirement_client_2,
        "non_retirement": data.non_retirement,
        "liabilities": data.liabilities
    }

    # Render HTML String for SACS (Browser Native Print Strategy)
    return templates.TemplateResponse(request=request, name="sacs_report.html", context=template_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
