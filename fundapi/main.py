from fastapi import FastAPI
from fundapi.routers.router import router as fund_router

app = FastAPI(docs_url="/")
app.include_router(fund_router)
