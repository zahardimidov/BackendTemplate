from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api import router
from app.bot import init_bot
from app.infra.admin import Admin
from app.infra.database.session import engine, run_database


async def on_startup(app: FastAPI):
    await init_bot(app)
    await run_database()
    yield


async def redirect_to_docs():
    return RedirectResponse(url="/docs")

app = FastAPI(lifespan=on_startup)
app.include_router(router)

admin = Admin(base_url="/api/admin")
admin.init(app, engine)

app.add_api_route('/', endpoint=redirect_to_docs, methods=['get'], include_in_schema=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        '*'
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
