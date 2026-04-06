from fastapi import FastAPI
from app.api.v1 import routes


app = FastAPI(title={{project_name}})


@app.get("/")
def get_root():
    return {"message": "{{project_name}}"}


# register routes
app.include_router(routes, prefix="/api/v1")
