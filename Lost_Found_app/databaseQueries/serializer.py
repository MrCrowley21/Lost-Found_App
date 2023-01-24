import graphene
from django_filters import FilterSet, OrderingFilter
from graphene import relay
from graphene_django import DjangoObjectType

from .models import Chat, Message


class ChatFilter(FilterSet):
    class Meta:
        model = Chat
        fields = ("last_modified", "name")
        order_by = ("last_modified", 'name', "id")


class ChatType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = Chat
        fields = '__all__'
        interfaces = (relay.Node,)


class MessageFilter(FilterSet):
    class Meta:
        model = Message
        fields = ("read", "deleted")
        order_by = ("id", 'created')


class MessageType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = Message
        fields = '__all__'
        interfaces = (relay.Node,)
