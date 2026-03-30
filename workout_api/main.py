from fastapi import FastAPI
from fastapi_pagination import add_pagination
from workout_api.routes import api_router

app = FastAPI(title="WorkoutApi")
add_pagination(app)
app.include_router(api_router, prefix="/api/v1")
if __name__ == 'main':
    import uvicorn 

    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)