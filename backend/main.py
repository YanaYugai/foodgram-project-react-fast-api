from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_paginate import add_pagination

from backend.src.auth import routers as auth
from backend.src.ingredients import routers as ingredients
from backend.src.recipes import routers as recipes
from backend.src.tags import routers as tags
from backend.src.users import routers as users

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
