import graphene
from User.schema import Query as UserQuery
from User.schema import Mutation as UserMutation

class Query(UserQuery, graphene.ObjectType):
    # Add any additional queries here
    pass

class Mutation(UserMutation, graphene.ObjectType):
    # Add any additional mutations here
    pass


# Create the GraphQL schema for User
schema = graphene.Schema(query=Query, mutation=Mutation)

