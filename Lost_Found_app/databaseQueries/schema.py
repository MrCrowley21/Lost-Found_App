from graphene import Mutation, ObjectType, List, Field, Int, String, ID
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from graphene_file_upload.scalars import Upload 
import graphql_jwt   

from datetime import datetime  


from .models import * 


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id',
            'last_login',
            'email', 
            'first_name',
            'last_name', 
            'is_active'
        ) 
class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile 
        ( 
            'user',
            'image' 
        )


class AnnouncementType(DjangoObjectType):
    class Meta:
        model = Announcement
        fields = ( 
            'id',
            'title',
            'user',
            'location',
            'image',
            'content',
            'reward', 
            'annType', 
            'tags', 
            'passed_time'
        )


class ChatSystem(DjangoObjectType):
    class Meta:
        model = Chat
        fields = (
            #'user_id', 
            'register_date',   
            'id', 
            'close_date'
        )


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = (
            #'sender_id',
            #'chat_id', 
            'id',
            'registered_date',
            'edited_date',
            'is_read',
            'content'
        )


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = (
            #'user_id', 
            'id', 
            #'announcement_id',
            'registered_date',
            'edited_date',
            'content'
        )


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = (
            'id', 
            'name'
        )


class Query(object):
    """
    User queries.
    """
    users = List(UserType)
    user = Field(UserType, id=Int())
    me = Field(UserProfileType) 
    user_profiles = List(UserProfileType)

    found_announcements = List(AnnouncementType) 
    announcements_search_by_content = List(AnnouncementType, search=String())
    lost_announcements = List(AnnouncementType)
    chats = List(ChatSystem)
    messages = List(MessageType)
    comments = List(CommentType)
    tags = List(TagType)  

    announcement = Field(AnnouncementType, id=Int())  

    announcements_by_tag = List(AnnouncementType,annType = String(),  tag = String())

    @staticmethod
    def resolve_users(self, info, **kwargs):
        """
        Resolves all users.
        """
        return User.objects.all() 

    def resolve_user_profiles(self, info, **kwargs):
        """
        Resolves all users.
        """
        return UserProfile.objects.all()

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
        return UserProfile.objects.get(user =user)

    @staticmethod
    def resolve_announcement(self, info, **kwargs):  
        obj = Announcement.objects.get(**kwargs) 
        obj.updateTimePassed()
        """
        Resolves a single Annoucnemnt
        """  
        return Announcement.objects.get(**kwargs)


    @staticmethod
    def resolve_found_announcements(self, info): 
        for obj in Announcement.objects.filter(annType__contains ="FOUND"):
            obj.updateTimePassed()
        return Announcement.objects.filter(annType__contains ="FOUND") 

    @staticmethod
    def resolve_announcements_search_by_content(self, info, search):
        for obj in  Announcement.objects.filter(content__icontains=search):
            obj.updateTimePassed()
        return Announcement.objects.filter(content__icontains=search)

    #@staticmethod
    def resolve_lost_announcements(self, info): 
        for obj in  Announcement.objects.filter(annType__contains ="LOST"):
            obj.updateTimePassed()
        return Announcement.objects.filter(annType__contains ="LOST")

    @staticmethod
    def resolve_announcements_by_tag(self, info, annType, tag ):  
        try:
            for obj in  Announcement.objects.filter(annType__contains = annType, tags = Tag.objects.get(name=tag)):
                obj.updateTimePassed()
            return Announcement.objects.filter(annType__contains = annType, tags = Tag.objects.get(name=tag))
        except:
            pass 


    @staticmethod
    def resolve_tags(self, info):
        return Tag.objects.all()

    @staticmethod
    def resolve_chats(self, info):
        return Chat.objects.all()

    @staticmethod
    def resolve_messages(self, info):
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

    class Arguments:
        """
        Input arguments to create a user.
        """
        email = String(required=True)
        password = String(required=True)

    @staticmethod
    def mutate(_, info, email, password):
        """
        Use the create_user method and return the
        attributes we specified.
        """
        user = User.objects.create_user(email=email,
                                        password=password,
                                        )
        return CreateUser( id=user.id ) 

class CreateAnnouncement(Mutation):
    id = ID()

    class Arguments: 
        title = String(required=True)
        user_id = Int(required=True)
        location = String(required=True)
        image = Upload(required=False)
        content = String(required=True)  
        reward = Int(required=False) 
        annType = String(required=True) 
        tag = String(required=True)

    announce = Field(AnnouncementType) 
    @staticmethod
    def mutate(_, info,title, image,  user_id,  location,  content, reward, annType,tag):
        announce = Announcement(   
            title =  title,
            image = image, 
            user =  UserProfile.objects.get(id = user_id), 
            location =  location,
            content =  content, 
            annType = annType, 
            reward = reward, 
            created_time = datetime.now()
            ) 
        announce.save() 
        try:    
            tagObj = Tag.objects.get(name=tag) 
        except:
            tagObj = Tag(name=tag)
            tagObj.save()
        announce.tags.add(tagObj)
        return CreateAnnouncement( 
            id = announce.id
        ) 


class DeleteFoundAnnouncement(Mutation):
    id = ID()
    class Arguments: 
        ann_id = Int(required=True)

    announce = Field(AnnouncementType) 
    @staticmethod
    def mutate(_, info,  ann_id):
        Announcement.objects.get(id = ann_id ).delete()  
        return DeleteFoundAnnouncement( 
            id = ann_id
        )


class UpdateFoundAnnouncement(Mutation): 
    id = ID() 

    class Arguments: 
        ann_id = Int(required=True )
        location = String(required=True)
        image = Upload(required=False)
        content = String(required=True)  
        reward = Int(required=False)


    announce = Field(AnnouncementType)
    @staticmethod
    def mutate(_,  info, ann_id, location, image, content, reward):
        announce = Announcement.objects.get(id=ann_id)  
        announce.location = location 
        if image is not None:
            announce.image = image
        announce.content = content  
        if reward is not None:
            announce.reward = reward
        announce.save()
        return UpdateFoundAnnouncement( id = announce.id ) 



# class CreateLostAnnouncement(Mutation):
#     id = ID()

#     class Arguments:
#         user_id = Int(required=True)
#         #tags = List(String)
#         location = String(required=True)
#         image = Upload(required=False)
#         content = String(required=True)
#         reward = Int(required=False)

#     announce = Field(LostAnnouncement)
#     @staticmethod
#     def mutate(_, info, image,  user_id,  location,  content, reward):
#         announce = Announcement(
#             #tags = tags,
#             image=image,
#             user_id=UserProfile.objects.get(id=user_id),
#             location=location,
#             content=content,
#             reward=reward
#             )
#         announce.save()
#         return CreateLostAnnouncement(
#             id=announce.id
#         )


# class DeleteLostAnnouncement(Mutation):
#     id = ID()
#     class Arguments:
#         id_ann = Int(required=True)

#     announce = Field(LostAnnouncement)
#     @staticmethod
#     def mutate(_, info,  id_ann):
#         announce = Announcement.objects.get(id=id_ann).delete()
#         return DeleteLostAnnouncement(
#             id=id_ann
#         )


# class UpdateLostAnnouncement(Mutation):
#     id = ID()
#     msg = String()

#     class Arguments:
#         ann_id = Int(required=True )
#         #user_id = Int(required=True)
#         #tags = List(String)
#         location = String(required=True)
#         image = Upload(required=False)
#         content = String(required=True)
#         reward = Int(required=False)

#     announce = Field(LostAnnouncement)
#     @staticmethod
#     def mutate(_,  info, ann_id, location, image, content, reward):
#         announce = Announcement.objects.get(id=ann_id)
#         announce.location = location
#         if image is not None:
#             announce.image = image
#         announce.content = content 
#         announce.reward = reward 
#         announce.save()
#         return UpdateLostAnnouncement(id=announce.id, msg="Success")


class CreateChat(Mutation):
    id = ID()

    class Arguments:
        user_id = Int(required=True)

    chat = Field(ChatSystem)
    @staticmethod
    def mutate(_, info, user_id): 
        chat = Chat(
            user_id=UserProfile.objects.get(id=user_id), 
            # register_date = datetime.now() 
            )  
        chat.save() 
        return CreateChat(
            id=chat.id
        )


class UpdateChat(Mutation):
    id = ID()

    class Arguments:
        chat_id = Int(required=True)

    announce = Field(ChatSystem)
    @staticmethod
    def mutate(_,  info, chat_id):
        chat = Chat.objects.get(id=chat_id)
        chat.close_date = datetime.now() 
        chat.save()
        return UpdateChat(id=chat.id) 





##################### COMMENTS ########################################################   
class CreateComment(Mutation):
    id = ID()

    class Arguments: 
        announcement_id = Int(required=True) 
        user_id =  Int(required=True)
        content = String(required=True)

    comment = Field(CommentType) 
    @staticmethod
    def mutate(_, info, announcement_id, content,user_id ):
        comment = Comment(   
            user_id  =  UserProfile.objects.get(id=user_id),  
            content =  content,  
            announcement_id = Announcement.objects.get( id = announcement_id)  )
        comment.save()   
        return CreateComment( 
            id = comment.id
        )  

class EditComment(Mutation): 
    id = ID()
    content = String()

    class Arguments:  
        comment_id = Int(required=True)
        content = String(required=True)

    comment = Field(CommentType) 
    @staticmethod
    def mutate(_, info, comment_id, content ): 
        comment = Comment.objects.get(id = comment_id )
        comment.content = content 
        comment.edited_time = datetime.now()
        comment.save()   
        return EditComment(  
            id = comment.id, 
            content = comment.content
        ) 

class DeleteComment(Mutation):
    msg  = String()
    class Arguments:  
        comment_id = Int(required=True)
    comment = Field(CommentType) 
    @staticmethod
    def mutate(_, info, comment_id): 
        comment = Comment.objects.get(id = comment_id ).delete()
        return DeleteComment( 
            msg = "Comment Deleted succesfully"
        )

############################# Message ###############################################   
class CreateMessage(Mutation):
    id = ID()
    class Arguments: 
        chat_id = Int(required=True) 
        sender_id = Int(required=True)
        content = String(required=True) 

    message = Field(MessageType) 
    @staticmethod
    def mutate(_, info, chat_id, content,sender_id ):
        message = Message(   
            sender_id  =   UserProfile.objects.get(id=sender_id),   
            content =  content, 
            chat_id = Chat.objects.get( id = chat_id), 
            registered_time = datetime.now(),
             )
        message.save()   
        return CreateMessage( 
            id = message.id
        )  

class EditMessage(Mutation):
    content = String()
    class Arguments:  
        message_id = Int(required=True)
        content = String(required=True)

    message = Field(MessageType) 
    @staticmethod
    def mutate(_, info, message_id, content ): 
        message = Message.objects.get(id = message_id )
        message.content = content 
        message.edited_time = datetime.now()
        message.save()   
        return EditMessage( 
            content = message.content
        )  

class DeleteMessage(Mutation):
    msg  = String()
    class Arguments:  
        message_id = Int(required=True)
    message = Field(MessageType) 
    @staticmethod
    def mutate(_, info, message_id): 
        message = Message.objects.get(id = message_id ).delete()
        return DeleteMessage( 
            msg = "Message Deleted succesfully"
        )

        
class CreateTags(Mutation):
    msg = String()
    class Arguments:
        tag_list = List(String, required=True)

    tag = Field(TagType)
    @staticmethod
    def mutate(_, info, tag_list): 
        idString = ""
        for tag_name in tag_list: 
            try:
                tag = Tag.objects.get(name = tag_name)
                idString += f"{tag_name} already exist. "   
            except:
                tag = Tag(
                    name=tag_name
                    )  
                idString += f"Tag {tag_name} have been created."
                tag.save() 
        return CreateTags( 
            msg = idString
        )
 

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
    create_new_announcement = CreateAnnouncement.Field() 
    update_announcement = UpdateFoundAnnouncement.Field() 
    delete_announcement = DeleteFoundAnnouncement.Field() 

    """ 
     Mutations for Creating and Updating Chat 
    """ 

    create_chat = CreateChat.Field() 
    update_chat = UpdateChat.Field()  

    """
    Mutations for Creating and Updating Comments
    """ 
    create_comment = CreateComment.Field() 
    edit_comment = EditComment.Field() 
    delete_comment = DeleteComment.Field()  
    """
    Mutations for Creating and Updating Message 
    """   
    create_message = CreateMessage.Field() 
    edit_message = EditMessage.Field() 
    delete_message = DeleteMessage.Field()  

    """
    Mutation Tags 
    """ 
    create_tags = CreateTags.Field()







