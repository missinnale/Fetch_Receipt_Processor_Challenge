from datetime import date
from typing import Annotated
from pydantic import BaseModel, Field

class Item(BaseModel, populate_by_name=True):
    short_description: Annotated[str, Field(
        alias="shortDescription",
        pattern=r"^[\w\s\-]+$", 
        examples=["Mountain Dew 12PK"],
        description="The Short Product Description for the item."
    )]
    price: Annotated[str, Field(
        pattern=r"^\d+\.\d{2}$",
        examples=["6.49"],
        description="The total price paid for this item."
    )]

class Receipt(BaseModel, populate_by_name=True):
    retailer: Annotated[str, Field(
        pattern=r"^[\w\s\-&]+$",
        examples=["M&M Corner Market"],
        description="The name of the retailer or store the receipt is from."
    )]
    purchase_date: Annotated[date, Field(
        alias="purchaseDate",
        examples=["2022-01-01"],
        description="The date of the purchase printed on the receipt.",
    )]
    purchase_time: Annotated[str, Field(
        alias="purchaseTime",
        pattern=r"^\d{2}:\d{2}$",
        examples=["13:01"],
        description="The time of the purchase printed on the receipt. 24-hour time expected."
    )]
    items: list[Item]
    total: Annotated[str, Field(pattern=r"^\d+\.\d{2}$", examples=["6.49"])]