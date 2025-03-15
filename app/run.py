import os
import sys

from fastapi.responses import RedirectResponse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.bot import process_update, run_bot_webhook
from app.config import WEBHOOK_PATH
from app.infra.admin import Admin
from app.infra.database.session import engine, run_database


async def on_startup(_):
    await run_database()
    await run_bot_webhook()
    yield


async def redirect_to_docs():
    return RedirectResponse(url="/docs")

app = FastAPI(lifespan=on_startup)
app.include_router(router)

admin = Admin(base_url="/api/admin")
admin.init(app, engine)

app.add_api_route(WEBHOOK_PATH, endpoint=process_update, methods=['post'])
app.add_api_route('/', endpoint=redirect_to_docs, methods=['get'], include_in_schema=False)
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        '*'
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, forwarded_allow_ips='*')
