import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from config import config
from app.controllers import router
from database import initiate_database

app = FastAPI(
    title=config['PROJECT_NAME'],
    openapi_url=f"{config['API_V1_STR']}/openapi.json",
    docs_url=None,
    redoc_url=None,
)
app.include_router(router, prefix=config['API_V1_STR'])

if config['SHOW_API_DOC']:
    app.mount("/static", StaticFiles(directory="./static"), name="static")


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


@app.get("/api", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Ti-Portal app."}

@app.on_event("startup")
async def start_database():
    await initiate_database()


if __name__ == "__main__":
    uvicorn.run('app.__main__:app', host=config['HOST'], port=config['PORT'], reload=True, debug=config['DEBUG'],
                workers=config['WORKERS'])
