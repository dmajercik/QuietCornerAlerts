import fastapi
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import incidentmanager, cad, usermanager, addressmanager, personmanager

app = fastapi.FastAPI(
    title="Quiet Corner Alerts API",
    description="The backend API for the Quiet Corner Alerts CAD system",
    version="0.0.1"
)

app.include_router(incidentmanager.router)
# app.include_router(cad.router)
app.include_router(usermanager.router)
app.include_router(personmanager.router)
app.include_router(addressmanager.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3321)
