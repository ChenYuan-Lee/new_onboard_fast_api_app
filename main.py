from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from ariadne.asgi import GraphQL
from ariadne import make_executable_schema, load_schema_from_path, format_error, UnionType
from graphql import GraphQLError

from graphql_objects import DatesCheck, GenericError, ListingUnsupportedError
from resolvers import query

dates_result = UnionType("DatesResult")


@dates_result.type_resolver
def resolve_ranked_search_type(obj, *_):
    if isinstance(obj, DatesCheck):
        return "DatesCheck"
    if isinstance(obj, GenericError):
        return "GenericError"
    if isinstance(obj, ListingUnsupportedError):
        return "ListingUnsupportedError"
    return None


schema_definition = load_schema_from_path("schema.graphql")
executable_schema = make_executable_schema(schema_definition, query, dates_result)


def custom_error_formatter(error: GraphQLError, debug: bool) -> dict:
    if debug:
        return format_error(error, debug)

    formatted = error.formatted
    formatted["message"] = "CUSTOM TOY APP ERROR"
    formatted["debug"] = repr(error)
    return formatted


app = FastAPI(debug=True, default_response_class=ORJSONResponse)
app.mount("/graphql", GraphQL(executable_schema, error_formatter=custom_error_formatter, debug=True))
