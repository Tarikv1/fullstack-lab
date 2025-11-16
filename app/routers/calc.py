from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/calc", tags=["calc"])


@router.get("/sum")
def sum_numbers(a: int | None = None, b: int | None = None):
    if a is None or b is None:
        raise HTTPException(status_code=400, detail="Both 'a' and 'b' query params are required")
    return {"result": a + b}
