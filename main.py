from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from ariadne.asgi import GraphQL
from ariadne import make_executable_schema, load_schema_from_path, UnionType

from resolvers import query


schema_definition = load_schema_from_path("schema.graphql")
executable_schema = make_executable_schema(schema_definition, query)

app = FastAPI(debug=True, default_response_class=ORJSONResponse)
app.mount("/graphql", GraphQL(executable_schema))
