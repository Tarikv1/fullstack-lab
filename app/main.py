from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/sum")
def sum_numbers(
    a: float = Query(..., description="First number"),
    b: float = Query(..., description="Second number")
):
    return {"result": a + b}
