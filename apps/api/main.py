from fastapi import FastAPI, HTTPException
from data_store import SISMOS

app = FastAPI(title="Datos Sismos")

@app.get("/sismos/{sismo_id}")
def get_sismo(sismo_id: str):
    sismo = SISMOS.get(sismo_id)
    if not sismo:
        raise HTTPException(status_code=404, detail="Sismo no encontrado")
    return sismo
