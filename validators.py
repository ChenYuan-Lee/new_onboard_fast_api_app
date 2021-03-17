from pydantic import BaseModel, conlist, conint, Field


class ListingsCheckInputValidator(BaseModel):
    listing_ids: conlist(conint(gt=0), min_items=1) = Field(
        title="Listing ids to check on"
    )