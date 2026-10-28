from fastapi import FastAPI

from app.monitoring import (
    analyze_monitoring_status,
    DATABASE
)


app = FastAPI(
    title="Industrial AI Monitoring API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Industrial AI Monitoring API is running"
    }


@app.get("/monitoring")
def get_monitoring_status():
    """
    Return the current production monitoring status.
    """

    result = analyze_monitoring_status(
        DATABASE
    )

    return result