from fastapi import FastAPI, Request, status
from backend.src.recipes import routers as recipes
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from backend.src.ingredients import routers as ingredients


app = FastAPI()


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Не все данные были представлены"},
    )


app.include_router(recipes.router)
app.include_router(ingredients.router)
