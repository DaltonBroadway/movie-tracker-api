from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.handlers import demo, movie_v1
from api.middleware import CustomHeaderMiddleware, PrometheusMiddleware


def create_app():
    app = FastAPI(docs_url="/")

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # app.add_middleware(CustomHeaderMiddleware, test_option=True)
    PrometheusMiddleware(app=app)

    # Routers
    # app.include_router(demo.router)
    app.include_router(movie_v1.router)

    return app
