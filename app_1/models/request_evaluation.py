from pydantic import BaseModel

class RequestEvaluation(BaseModel):
    int_rate: float
    put_prncp: float
    tota_rec_prncp: float
    last_pymnt_amnt:float
    addr_state: str
    grade: str
    sub_grade: str
    total_pymn: float