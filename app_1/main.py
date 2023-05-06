from fastapi import FastAPI
from app_1.models import RequestEvaluation
import pandas as pd

app=FastAPI()

@app.get("/health")
def health_check():
    return{"is_alive": True}

@app.post("/evaluate")
async def evaluate(req: RequestEvaluation):
    print(req)
    df=pd.dataFrame({
        "int_rate":[req.int_rate],
        "out_prncp": [req.out_prncp],
        "total_req_prncp":[req.total_req_prncp],
        "last_pymnt_amnt": [req.last_pymnt_amnt],
        "addr_state": [req.addr_state],
        "grade": [req.grade],
        "sub_grade": [req.sub_grade],
        "total_pymn": [req.total_pymn],
    })

