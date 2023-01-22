from graphene import Mutation, ObjectType, List, Field, Int, String, ID
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from graphene_file_upload.scalars import Upload 
import graphql_jwt   

from datetime import datetime   


from .remote_api import RemoteAPI
from .encryption import Encryption

from .models import * 

api = RemoteAPI() 
enc = Encryption()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id',
            'email', 
            'first_name',
            'last_name', 
        ) 
class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile 
        (   'user', 
            'location',
            'image', 
            'phone',
            'date_of_birth', 
            'rating'
        ) 

class AnnouncementType(DjangoObjectType):
    class Meta:
        model = Announcement
        fields = ( 
            'id',
            'title',
            'user_profile',
            'street_name',
            'coordonates', 
            'image',
            'content',
            'reward', 
            'annType', 
            'tags', 
            'passed_time'
        )


############################### STILL NOT

# class ChatSystem(DjangoObjectType):
#     class Meta:
#         model = Chat
#         fields = (
#             'register_date',   
#             'id', 
#             'close_date'
#         )


# class MessageType(DjangoObjectType):
#     class Meta:
#         model = Message
#         fields = (
#             #'sender_id',
#             #'chat_id', 
#             'id',
#             'registered_date',
#             'edited_date',
#             'is_read',
#             'content'
#         )


# class CommentType(DjangoObjectType):
#     class Meta:
#         model = Comment
#         fields = (
#             #'user_id', 
#             'id', 
#             #'announcement_id',
#             'registered_date',
#             'edited_date',
#             'content'
#         )


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
    user_profile = Field(UserProfileType, id = Int()) 
    me = Field(UserProfileType) 
    
    announcement = Field(AnnouncementType, id=Int()) 
    found_announcements = List(AnnouncementType)  
    lost_announcements = List(AnnouncementType) 
    announcements_search_by_content = List(AnnouncementType, search=String())  
    announcements_by_tag = List(AnnouncementType,annType = String(),  tag = String()) 

    tags = List(TagType) 

    # chats = List(ChatSystem)
    # messages = List(MessageType)
    # comments = List(CommentType) 


    @staticmethod
    def resolve_users(self, info, **kwargs):
        return User.objects.all() 

    @staticmethod
    def resolve_user(self, info, **kwargs):
        return User.objects.get(**kwargs) 

    @staticmethod
    def resolve_user_profile(self, info, id):
        return UserProfile.objects.get(user_id = id)


    @staticmethod
    def resolve_me(self, info):
        user = info.context.user 
        if user.is_anonymous:
            raise Exception('You are not logged in')
        return UserProfile.objects.get(user =user)

    @staticmethod
    def resolve_announcement(self, info, **kwargs):  
        obj = Announcement.objects.get(**kwargs) 
        obj.updateTimePassed()
        obj.save()
        return obj 


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
            for obj in  Announcement.objects.filter(annType__contains = annType.upper(), tags = Tag.objects.get(name=tag)):
                obj.updateTimePassed()
            return Announcement.objects.filter(annType__contains = annType.upper(), tags = Tag.objects.get(name=tag))
        except:
            pass 


    @staticmethod
    def resolve_tags(self, info):
        return Tag.objects.all()

    # @staticmethod
    # def resolve_chats(self, info):
    #     return Chat.objects.all()

    # @staticmethod
    # def resolve_messages(self, info):
    #     return Message.objects.all()

    # @staticmethod
    # def resolve_comments(self, info):
    #     return Comment.objects.all()


class CreateUser(Mutation):
    id = ID()

    class Arguments:
        email = String(required=True)
        password = String(required=True)

    @staticmethod
    def mutate(_, info, email, password):
        user = User.objects.create_user(email=email,
                                        password=password,
                                        )
        return CreateUser( id=user.id )  


        

class CreateAnnouncement(Mutation):
    id = ID()  
    msg = String()
    class Arguments: 
        title = String(required=True)
        street_name = String(required=True) 
        coordonates = String(required=True)
        image = Upload(required=False)
        content = String(required=True)  
        reward = Int(required=False) 
        annType = String(required=True) 
        tag = String(required=True)

    @staticmethod
    def mutate(_, info,title, image, street_name, coordonates,  content, reward, annType,tag): 
        user = info.context.user  
        if user.is_authenticated == False: 
              return CreateAnnouncement( 
            id = None,  
            msg = "You are not logged in in order to create the post!"
        ) 
        announce = Announcement(   
            title =  title,
            image = image, 
            user_profile =  UserProfile.objects.get(user = user), 
            street_name = street_name,
            coordonates = coordonates,
            content =  content, 
            annType = annType.upper(), 
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
            id = announce.id,
            msg = "Succesful"
        ) 


class DeleteAnnouncement(Mutation):
    id = ID()
    class Arguments: 
        ann_id = Int(required=True)
    @staticmethod
    def mutate(_, info,  ann_id):
        Announcement.objects.get(id = ann_id ).delete()  
        return DeleteAnnouncement( 
            id = ann_id
        )


class UpdateAnnouncement(Mutation): 
    id = ID()  
    msg = String()
    class Arguments: 
        ann_id = Int(required=True )
        street_name = String(required=False) 
        coordonates = String(required=False)
        image = Upload(required=False)
        content = String(required=True)  
        reward = Int(required=False) 
        title = String(required=False)


    @staticmethod
    def mutate(_,  info, ann_id, title, street_name, coordonates, image, content, reward): 
        user = info.context.user  
        if user.is_authenticated == False:
            return CreateAnnouncement( 
            id = None,  
            msg = "You are not logged in in order to create the post!")

        announce = Announcement.objects.get(id=ann_id)  
        if image is not None:
            announce.image = image
        announce.content = content  
        if reward is not None:
            announce.reward = reward 
        if street_name is not None:
            announce.street_name = street_name 
        if coordonates is not None:
            announce.coordonates = coordonates 
        if content is not None:
            announce.content = content 
        if reward is not None:
            announce.reward = reward 
        if title is not None:
            announce.title = title
        announce.save()
        return UpdateAnnouncement( id = announce.id, msg= "Succesful" )  





class UpdateUserProfile(Mutation): 
    api_msg = String() 
    msg = String()

    class Arguments: 
        image = Upload(required=False)
        date_of_birth = String(required=False) 
        phone_number = String(required = False)
        first_name = String(required = False )
        last_name = String(required = False)
        rating =  Int(required=False)

    @staticmethod
    def mutate(_,  info, image, date_of_birth, phone_number, first_name, last_name,rating): 
        user = info.context.user  
        if user.is_authenticated == False:
            return UpdateUserProfile( 
            api_msg = None, 
            msg = "You are not logged in in order to update user profile!")      


        usr_prof = UserProfile.objects.get(user=user)   
        apiMsg = None  
        
        if first_name and last_name is not None:    
            try:
                api_cred = ApiCredentials.objects.get(user_profile=usr_prof)  
                apiMsg = "Api User Credentials already exist"  
            except:
                try: 
                    kek = f'{first_name} {last_name}'
                    api_cred = ApiCredentials.objects.get(username = kek)  
                    apiMsg = "Api User Name  Credentials already exist"
                except:
                    res = api.create_user( first_name + " " + last_name )  
                    api_cred = ApiCredentials(
                                user_profile = usr_prof,
                                username = first_name + " " + last_name, 
                                remote_id = enc.aesCbcPbkdf2EncryptToBase64( user.password,  res["id"]),
                                secret = enc.aesCbcPbkdf2EncryptToBase64( user.password, res["secret"]),
                                created_at = res["created_at"]
                                )
                    api_cred.save() 
                    apiMsg = "Api User Created"
             
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if image is not None:
            usr_prof.image = image
        if date_of_birth is not None:
            usr_prof.date_of_birth = date_of_birth 
        if phone_number is not None:
            usr_prof.phone = phone_number  
        if rating is not None:
            usr_prof.rating = rating 
        
        
        usr_prof.save() 
        user.save() 

        return UpdateUserProfile(
                msg = "Succesful", 
                api_msg = apiMsg ) 



# class CreateChat(Mutation):
#     id = ID()

#     class Arguments:
#         user_id = Int(required=True)

#     chat = Field(ChatSystem)
#     @staticmethod
#     def mutate(_, info, user_id): 
#         chat = Chat(
#             user_id=UserProfile.objects.get(user_id=user_id), 
#             # register_date = datetime.now() 
#             )  
#         chat.save() 
#         return CreateChat(
#             id=chat.id
#         )


# class UpdateChat(Mutation):
#     id = ID()

#     class Arguments:
#         chat_id = Int(required=True)

#     #announce = Field(ChatSystem)
#     @staticmethod
#     def mutate(_,  info, chat_id):
#         chat = Chat.objects.get(id=chat_id)
#         chat.close_date = datetime.now() 
#         chat.save()
#         return UpdateChat(id=chat.id) 





##################### COMMENTS ########################################################   
# class CreateComment(Mutation):
#     id = ID()

#     class Arguments: 
#         announcement_id = Int(required=True) 
#         user_id =  Int(required=True)
#         content = String(required=True)

#     comment = Field(CommentType) 
#     @staticmethod
#     def mutate(_, info, announcement_id, content,user_id ):
#         comment = Comment(   
#             user_id  =  UserProfile.objects.get(user_id=user_id),  
#             content =  content,  
#             announcement_id = Announcement.objects.get( id = announcement_id)  )
#         comment.save()   
#         return CreateComment( 
#             id = comment.id
#         )  

# class EditComment(Mutation): 
#     id = ID()
#     content = String()

#     class Arguments:  
#         comment_id = Int(required=True)
#         content = String(required=True)

#     comment = Field(CommentType) 
#     @staticmethod
#     def mutate(_, info, comment_id, content ): 
#         comment = Comment.objects.get(id = comment_id )
#         comment.content = content 
#         comment.edited_time = datetime.now()
#         comment.save()   
#         return EditComment(  
#             id = comment.id, 
#             content = comment.content
#         ) 

# class DeleteComment(Mutation):
#     msg  = String()
#     class Arguments:  
#         comment_id = Int(required=True)
#     comment = Field(CommentType) 
#     @staticmethod
#     def mutate(_, info, comment_id): 
#         comment = Comment.objects.get(id = comment_id ).delete()
#         return DeleteComment( 
#             msg = "Comment Deleted succesfully"
#         )

# ############################# Message ###############################################   
# class CreateMessage(Mutation):
#     id = ID()
#     class Arguments: 
#         chat_id = Int(required=True) 
#         sender_id = Int(required=True)
#         content = String(required=True) 

#     message = Field(MessageType) 
#     @staticmethod
#     def mutate(_, info, chat_id, content,sender_id ):
#         message = Message(   
#             sender_id  =   UserProfile.objects.get(user_id=sender_id),   
#             content =  content, 
#             chat_id = Chat.objects.get( id = chat_id), 
#             registered_time = datetime.now(),
#              )
#         message.save()   
#         return CreateMessage( 
#             id = message.id
#         )  

# class EditMessage(Mutation):
#     content = String()
#     class Arguments:  
#         message_id = Int(required=True)
#         content = String(required=True)

#     message = Field(MessageType) 
#     @staticmethod
#     def mutate(_, info, message_id, content ): 
#         message = Message.objects.get(id = message_id )
#         message.content = content 
#         message.edited_time = datetime.now()
#         message.save()   
#         return EditMessage( 
#             content = message.content
#         )  

# class DeleteMessage(Mutation):
#     msg  = String()
#     class Arguments:  
#         message_id = Int(required=True)
#     message = Field(MessageType) 
#     @staticmethod
#     def mutate(_, info, message_id): 
#         message = Message.objects.get(id = message_id ).delete()
#         return DeleteMessage( 
#             msg = "Message Deleted succesfully"
#         )

        
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
    User Profiles
    """
    
    update_user_profile = UpdateUserProfile.Field()

    """
    Mutations for Creating and Updating Announcement
    """ 
    create_new_announcement = CreateAnnouncement.Field() 
    update_announcement = UpdateAnnouncement.Field() 
    delete_announcement = DeleteAnnouncement.Field() 

    """ 
     Mutations for Creating and Updating Chat 
    """ 

    # create_chat = CreateChat.Field() 
    # update_chat = UpdateChat.Field()  

    """
    Mutations for Creating and Updating Comments
    """ 
    # create_comment = CreateComment.Field() 
    # edit_comment = EditComment.Field() 
    # delete_comment = DeleteComment.Field()  
    """
    Mutations for Creating and Updating Message 
    """   
    # create_message = CreateMessage.Field() 
    # edit_message = EditMessage.Field() 
    # delete_message = DeleteMessage.Field()  

    """
    Mutation Tags 
    """ 
    create_tags = CreateTags.Field() 







