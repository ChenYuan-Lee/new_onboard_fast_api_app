from typing import List

from ariadne import QueryType

from constants import LISTINGS_LOADER_NAME
from graphql_objects import ListingsCheck
from handler import Handler
from loader import ListingsLoader
from validators import ListingsCheckInputValidator

query = QueryType()


class QueryResolvers:

    @staticmethod
    @query.field("listings_check")
    async def get_listings_check(
            _,
            info,
            **search_criteria
    ) -> List[ListingsCheck]:
        validated_search_criteria = ListingsCheckInputValidator(**search_criteria)
        return await Handler.serve(
            info=info,
            search_criteria=validated_search_criteria
        )
