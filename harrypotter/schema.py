import graphene
import graphql_jwt
import characters.schema
import users.schema
import characters.schema_relay

class Query(
    users.schema.Query,
    characters.schema.Query,
    characters.schema_relay.RelayQuery,
    graphene.ObjectType,
):
    pass

class Mutation(
    users.schema.Mutation,
    characters.schema.Mutation,
    characters.schema_relay.RelayMutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)