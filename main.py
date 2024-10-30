from fastapi import FastAPI
from domain.client import client_router

app = FastAPI()

app.include_router(client_router.router)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(router, host="0.0.0.0", port=8001)