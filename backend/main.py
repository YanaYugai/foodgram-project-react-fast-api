from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_paginate import add_pagination

from src.auth import routers as auth
from src.ingredients import routers as ingredients
from src.recipes import routers as recipes
from src.tags import routers as tags
from src.users import routers as users

app = FastAPI()


@app.exception_handler(RequestValidationError)
def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Не все данные были представлены"},
    )


app.include_router(recipes.router)
app.include_router(ingredients.router)
app.include_router(tags.router)
app.include_router(users.router)
app.include_router(auth.router)
add_pagination(app)
