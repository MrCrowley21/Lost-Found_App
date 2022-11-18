import graphene
import databaseQueries.schema
class Query(databaseQueries.schema.Query, graphene.ObjectType):
    """
    Projects main Query class, this will inherit multiple queries.
    """
    pass 
class Mutation(databaseQueries.schema.Mutation, graphene.ObjectType):
    """
    Projects main Mutation class, this will 
    inherit multiple mutations.
    """
    pass
schema = graphene.Schema(query=Query, mutation=Mutation)