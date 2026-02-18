import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from b_e.config import config
from b_e.app.controllers import router
from b_e.database import init_database, test_db, engine, Base
from b_e.helpers.security_jwt.security_jwt import generate_rsa_key
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    await generate_rsa_key()
    await init_database()
    await test_db()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=config['PROJECT_NAME'],
    openapi_url=f"{config['API_V1_STR']}/openapi.json",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)
# app.mount(
#     "b_e/app/template/preview/static",
#     StaticFiles(directory=Path(__file__).parent.parent.absolute() / "b_e/app/template/preview/static"),
#     name="static"
# )

app.include_router(router, prefix=config['API_V1_STR'])

if config['SHOW_API_DOC']:
    script_dir = os.path.dirname(__file__)
    st_abs_file_path = os.path.join(script_dir, "static/")
    app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")


    @app.get("/api/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )


    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    # @app.get("/redoc", include_in_schema=False)
    # async def redoc_html():
    #     return get_redoc_html(
    #         openapi_url=app.openapi_url,
    #         title=app.title + " - ReDoc",
    #         redoc_js_url="/static/redoc.standalone.js",
    #     )



if __name__ == "__main__":
    uvicorn.run("b_e.app.__main__:app", host=config['HOST'], port=config['PORT'], reload=True,
                workers=config['WORKERS'], )
