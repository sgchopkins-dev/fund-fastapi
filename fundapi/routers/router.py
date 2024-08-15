from fastapi import APIRouter
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from fundapi.models.model import FundModel, UpdateFundModel, PyObjectId
import motor.motor_asyncio
import os
from typing import List

from dotenv import load_dotenv
load_dotenv()

MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
MONGODB_DB = os.getenv('MONGODB_DB')
MONGODB_SERVER = os.getenv('MONGODB_SERVER')

DB_URL = ("mongodb+srv://"
          + MONGODB_USERNAME 
          + ":" 
          + MONGODB_PASSWORD 
          + "@" 
          + MONGODB_SERVER 
          + "/?retryWrites=true&w=majority"
          )


client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
db = client.invest


router = APIRouter()


@router.get(
    "/funds", response_description="List all funds", response_model=List[FundModel]
)
async def list_funds():
    funds = await db["funds"].find().to_list(1000)
    return funds

@router.get(
    "/id/{id}", response_description="Get a single fund", response_model=FundModel
)
async def show_fund(id: PyObjectId):
    if (fund := await db["funds"].find_one({"_id": id})) is not None:
        return fund

    raise HTTPException(status_code=404, detail=f"Fund {id} not found")

@router.get(
    "/name/{name}", response_description="Search by Name", response_model=List[FundModel]
)
async def get_funds_by_name(name: str):
    funds = await db["funds"].find({"name": {'$regex': name, '$options': 'i'}}).to_list(1000)
    return funds


@router.post("/", response_description="Add new Fund", response_model=UpdateFundModel)
#async def create_fund(fund: FundModel = Body(...)):
async def create_fund(fund: UpdateFundModel = Body(...)):
    fund = jsonable_encoder(fund)
    new_fund = await db["funds"].insert_one(fund)
    created_fund = await db["funds"].find_one({"_id": new_fund.inserted_id})
    created_fund['_id'] = str(created_fund['_id'])
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_fund)


@router.put("/{id}", response_description="Update a fund", response_model=FundModel)
async def update_fund(id: PyObjectId, fund: UpdateFundModel = Body()):
    fund = {k: v for k, v in fund.dict().items() if v is not None}

    if len(fund) >= 1:
        update_result = await db["funds"].update_one({"_id": id}, {"$set": fund})

        if update_result.modified_count == 1:
            if (
                updated_fund := await db["funds"].find_one({"_id": id})
            ) is not None:
                return updated_fund

    if (existing_fund := await db["funds"].find_one({"_id": id})) is not None:
        return existing_fund

    raise HTTPException(status_code=404, detail=f"Fund {id} not found")


@router.delete("/{id}", response_description="Delete a fund")
async def delete_fund(id: PyObjectId):
    delete_result = await db["funds"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Fund {id} not found")

