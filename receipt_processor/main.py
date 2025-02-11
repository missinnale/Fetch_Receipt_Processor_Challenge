from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from receipt_processor.routes import receipts

app = FastAPI()

app.include_router(receipts.router)

# Reset Validation Error for malformed request data to a 400 instead of 422 to match given schema
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}