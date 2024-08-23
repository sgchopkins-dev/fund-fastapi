from fastapi import FastAPI
from fundapi.routers.router import router as fund_router

app = FastAPI(docs_url="/", ssl_keyfile="/etc/tls/tls.key", ssl_certfile="/etc/tls/tls.crt")
app.include_router(fund_router)
