from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
# from routes.weather_forecast import router as forecast_conditions
# from routes.wind_coastal_waters import router as wind_coastal_waters
from weather_app_api import weather_forecast, wind_coastal_waters

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(weather_forecast)
app.include_router(wind_coastal_waters)

@app.get("/")
def read_root():
    return {"message": "Welcome to the weather api"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)