from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from iscram.domain.model import SystemGraph
from iscram.service_layer import services
from iscram.adapters.repository import FakeRepository

app = FastAPI()
origins = ["http://localhost",
           "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

repo = FakeRepository()


@app.post("/risk")
async def risk(sg: SystemGraph = Body(...)):
    return {"risk": services.get_risk(sg, repo)}


@app.post("/birnbaum-structural-importances")
async def birnbaum_structural_importances(sg: SystemGraph = Body(...)):
    return {"birnbaum_structural_importances": services.get_birnbaum_structural_importances(sg, repo)}


@app.post("/birnbaum-importances")
async def birnbaum_importances(sg: SystemGraph = Body(...)):
    return {"birnbaum_importances": services.get_birnbaum_importances(sg, repo)}


@app.post("/attribute/{att}/{val}/birnbaum-structural-importances")
async def attr_birnbaum_structural_importances(att, val, sg: SystemGraph = Body(...)):
    try:
        selector = services.selector(att, bool(int(val)))
    except ValueError:
        return {"message": "Error: attribute value must be of integer type."}

    return services.get_birnbaum_structural_importances_select(sg, selector, repo)


@app.post("/attribute/{att}/{val}/birnbaum-importances")
async def attr_birnbaum_importances(att, val, sg: SystemGraph = Body(...)):
    selector = services.selector(att, bool(val))
    return services.get_birnbaum_importances_select(sg, selector, repo)


@app.post("/fractional_importance_traits")
async def fractional_importance_traits(sg: SystemGraph = Body(...)):
    return services.get_fractional_importance_traits(sg)


@app.get("/status")
async def status():
    return {"status": "alive"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7913, timeout_keep_alive=300, log_level="trace")