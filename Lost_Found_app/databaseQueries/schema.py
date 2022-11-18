from graphene import Mutation, ObjectType, List, Field, Int, String, ID
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from graphene_file_upload.scalars import Upload
import datetime
import graphql_jwt

from .models import *


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'last_login',
            'email',
            'is_active',
        )


class FoundAnnouncement(DjangoObjectType):
    class Meta:
        model = Announcement
        fields = (
            'announcement_id',
            'user_id',
            #'tags',
            'location',
            'image',
            'content'
        )


class LostAnnouncement(DjangoObjectType):
    class Meta:
        model = Announcement
        fields = (
            'announcement_id',
            'user_id',
            #'tags',
            'location',
            'image',
            'content',
            'reward'
        )


class ChatSystem(DjangoObjectType):
    class Meta:
        model = Chat
        fields = (
            'user_id',
            'register_date',
            'close_date'
        )


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = (
            'sender_id',
            'chat_id',
            'registered_date',
            'edited_date',
            'is_read',
            'content'
        )


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = (
            'user_id',
            'announcement_id',
            'registered_date',
            'edited_date',
            'content'
        )


class Query(object):
    """
    User queries.
    """
    users = List(UserType)
    user = Field(UserType, id=Int())
    me = Field(UserType)

    found_announcement = List(FoundAnnouncement) 
    found_ann_search = List(FoundAnnouncement, search = String())
    lost_announcement = List(LostAnnouncement)
    chats = List(ChatSystem)
    messages = List(MessageType)
    comments = List(CommentType) 

    @staticmethod
    def resolve_users(self, info, **kwargs):
        """
        Resolves all users.
        """
        return User.objects.all()

    @staticmethod
    def resolve_user(self, info, **kwargs):
        """
        Resolves a single user by ID.
        """
        return User.objects.get(**kwargs)

    @staticmethod
    def resolve_me(self, info):
        """
        Resolves the logged in user
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You are not logged in')
        return user

    @staticmethod
    def resolve_found_announcement(self, info):
        return Announcement.objects.all()

    @staticmethod
    def resolve_found_ann_search(self, info, search):
        return Announcement.objects.filter(title_icontains=search)

    @staticmethod
    def resolve_lost_announcement(self, info):
        return Announcement.objects.all()

    @staticmethod
    def resolve_chats(self, info):
        return Chat.objects.all()

    @staticmethod
    def resolve_message(self, info):
        return Message.objects.all()

    @staticmethod
    def resolve_comments(self, info):
        return Comment.objects.all()


class CreateUser(Mutation):
    """
    Create a user mutation.
    Attributes for the class define the mutation response.
    """
    id = ID()
    email = String()
    first_name = String()
    last_name = String()

    class Arguments:
        """
        Input arguments to create a user.
        """
        username = String(required=True)
        password = String(required=True)

    @staticmethod
    def mutate(_, info, username, password):
        """
        Use the create_user method and return the
        attributes we specified.
        """
        user = User.objects.create_user(username=username,
                                        password=password,
                                        )
        return CreateUser(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name)


class CreateFoundAnnouncement(Mutation):
    id = ID()

    class Arguments:
        user_id = Int(required=True)
        #tags = List(String)
        location = String(required=True)
        image = Upload(required=False)
        content = String(required=True)

    announce = Field(FoundAnnouncement) 
    @staticmethod
    def mutate(_, info, image,  user_id,  location,  content):
        announce = Announcement(   
            #tags = tags,  
            image = image, 
            user_id =  UserProfile.objects.get(id = user_id), 
            location =  location,
            content =  content
            )
        announce.save()   
        print(announce.id)
        return CreateFoundAnnouncement( 
            id = announce.id
        ) 


class DeleteFoundAnnouncement(Mutation):
    id = ID()
    class Arguments: 
        id_ann = Int(required=True)

    announce = Field(FoundAnnouncement) 
    @staticmethod
    def mutate(_, info,  id_ann):
        announce = Announcement.objects.get(id = id_ann ).delete()  
        return DeleteFoundAnnouncement( 
            id = id_ann
        )


class UpdateFoundAnnouncement(Mutation): 
    id = ID() 
    msg = String()

    class Arguments: 
        ann_id = Int(required=True )
        #user_id = Int(required=True)
        #tags = List(String)
        location = String(required=True)
        image = Upload(required=False)
        content = String(required=True)

    announce = Field(FoundAnnouncement)
    @staticmethod
    def mutate(_,  info, ann_id, location, image, content):
        announce = Announcement.objects.get(id=ann_id)  
        announce.location = location 
        if image is not None:
            announce.image = image
        announce.content = content
        announce.save()
        return UpdateFoundAnnouncement(id=announce.id, msg="Success")


class CreateLostAnnouncement(Mutation):
    id = ID()

    class Arguments:
        user_id = Int(required=True)
        #tags = List(String)
        location = String(required=True)
        image = Upload(required=False)
        content = String(required=True)
        reward = Int(required=False)

    announce = Field(LostAnnouncement)
    @staticmethod
    def mutate(_, info, image,  user_id,  location,  content, reward):
        announce = Announcement(
            #tags = tags,
            image=image,
            user_id=UserProfile.objects.get(id=user_id),
            location=location,
            content=content,
            reward=reward
            )
        announce.save()
        print(announce.id)
        return CreateLostAnnouncement(
            id=announce.id
        )


class DeleteLostAnnouncement(Mutation):
    id = ID()
    class Arguments:
        id_ann = Int(required=True)

    announce = Field(LostAnnouncement)
    @staticmethod
    def mutate(_, info,  id_ann):
        announce = Announcement.objects.get(id=id_ann).delete()
        return DeleteLostAnnouncement(
            id=id_ann
        )


class UpdateLostAnnouncement(Mutation):
    id = ID()
    msg = String()

    class Arguments:
        ann_id = Int(required=True )
        #user_id = Int(required=True)
        #tags = List(String)
        location = String(required=True)
        image = Upload(required=False)
        content = String(required=True)
        reward = Int(required=False)

    announce = Field(LostAnnouncement)
    @staticmethod
    def mutate(_,  info, ann_id, location, image, content):
        announce = Announcement.objects.get(id=ann_id)
        announce.location = location
        if image is not None:
            announce.image = image
        announce.content = content
        announce.save()
        return UpdateLostAnnouncement(id=announce.id, msg="Success")


class CreateChat(Mutation):
    id = ID()

    class Arguments:
        user_id = Int(required=True)

    announce = Field(ChatSystem)
    @staticmethod
    def mutate(_, info, user_id):
        chat = Chat(
            user_id=UserProfile.objects.get(id=user_id),
            register_date=datetime.datetime.now(),
            close_date=None
            )
        chat.save()
        print(chat.id)
        return CreateChat(
            id=chat.id
        )


class UpdateChat(Mutation):
    id = ID()
    msg = String()

    class Arguments:
        chat_id = Int(required=True)

    announce = Field(ChatSystem)
    @staticmethod
    def mutate(_,  info, chat_id):
        chat = Chat.objects.get(id=chat_id)
        chat.close_data = datetime.datetime.now()
        chat.save()
        return UpdateChat(id=chat.id, msg="Success")


class Mutation(ObjectType):
    """
    Mutations for Users.
    """
    create_user = CreateUser.Field()
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field() 

    """
    Mutations for Creating and Updating Announcement
    """
    create_new_announcement = CreateFoundAnnouncement.Field() 
    update_announcement = UpdateFoundAnnouncement.Field() 
    delete_found_announcement = DeleteFoundAnnouncement.Field()
