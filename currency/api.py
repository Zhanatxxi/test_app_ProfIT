from uvicorn import run
from fastapi import FastAPI

from currency.src.routes.api import api_v1

app = FastAPI(
    title="Currency application",
    description="Currency application for monitoring"
)

app.include_router(api_v1)


@app.get("/")
async def main():
    return "Welcome"


if __name__ == '__main__':
    run('api:app', reload=True, workers=4)
