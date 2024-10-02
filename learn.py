from enum import Enum
from typing import Any, Literal, Annotated
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field


class FilterQuery(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []



app = FastAPI(debug=True)


items = [i for i in range(101)]


class ItemId(BaseModel):
    index: int = Field(default=0, ge=0, le=len(items))

ItemId.index = Field(default=15, ge=1, le=len(items))

class MyModel(str, Enum):
    WINTER = "Winter"
    SPRING = "Spring"
    SUMMER = "Summer"
    AUTUMN = "Autumn"


@app.get("/models/{model_name}")
def get_model(model_name: MyModel):
    match model_name:
        case MyModel.AUTUMN:
            return {"model_name": model_name, "message": "Not the best time of year "}
        case MyModel.WINTER:
            return {"model_name": model_name, "message": "Ohhh, too many holidays"}
        case MyModel.SPRING:
            return {"model_name": model_name, "message": "So warm"}
        case _:
            return {"model_name": model_name, "message": "Zharko ochen'"}
    
    

@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/items")
def list_items(limit: int = Query(default=1, gt=0, le=len(items))) -> list[int]:
    return items[limit:]


# @app.get("/items/{item_id:path}")
# def item(item_id: str) -> int:
#     print(f"{item_id.split("/")=}")
#     item_id, operation = item_id.split("/")
#     item_id = int(item_id)
#     print(f"{operation=}")
#     return items[item_id]  -> So So
#   |
#   |
# @app.get("/items/{item_id}/details")
# def item_details(item_id: int) -> int:
#     return items[item_id] -> Do This

# @app.get("/items/{item_id}/details")
# def item_details(item_id: int, q=Query()) -> dict[str, int | Any]:
#     return {"result": items[item_id], "query": q}



@app.get("/items/details")
def item_details(item_id: Annotated[ItemId, Query()]) -> dict[str, int | Any]:
    return {"result": items[item_id.index]}