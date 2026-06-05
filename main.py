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
async def get_index(request: Request, client_id: Optional[int] = None):
    conn = sqlite3.connect("db.sqlite")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM clients')
    all_clients = [dict(row) for row in cursor.fetchall()]
    
    selected_client = None
    if client_id:
        cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
        row = cursor.fetchone()
        if row:
            selected_client = dict(row)
    conn.close()
    
    return templates.TemplateResponse(request=request, name="index.html", context={"all_clients": all_clients, "selected_client": selected_client})

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
