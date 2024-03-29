from graphene import Mutation, ObjectType, List, Field, Int, String, ID
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from graphene_file_upload.scalars import Upload 
import graphql_jwt    
import datetime    

from .remote_api import RemoteAPI
from .encryption import Encryption

from .models import *   

from .otp_sending import * 

import os

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

class OTPvType(DjangoObjectType):
    class Meta:
        model = OTPVerification
        fields = (
            'id',
            'secret', 
            'hotp') 
class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile 
        (   'user', 
            'location',
            'image', 
            'phone',
            'date_of_birth', 
            'rating', 
            'public_key'
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



class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = (
            'id', 
            'name'
        ) 


class ChatType(DjangoObjectType):
    class Meta:
        model = Chat
        fields = ( 
            'id',
            'name',
            'participants',
            'messages', 
            'key',
            'initiator', 
            'acceptor',
            'state'
        ) 


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = ( 
            'created',
            'sender',
            'text'
        )



class Query(ObjectType):
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

    chats = List(ChatType)
    chat = Field(ChatType, id=ID())
    messages = List(MessageType)


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

    @staticmethod
    def resolve_chats(cls, info, **kwargs):
        user = info.context.user  
        kek = UserProfile.objects.get(user=user)
        return Chat.objects.prefetch_related("messages", "participants").filter(participants=kek,state=1) | Chat.objects.prefetch_related("messages", "participants").filter(participants=kek,state=2,acceptor=user.email)

    @staticmethod
    def resolve_chat(cls, info, id, **kwargs):
        user = info.context.user
        return Chat.objects.prefetch_related("participants").get(participants=UserProfile.objects.get(user=user), id=id)

    @staticmethod
    def resolve_messages(cls, info, id, **kwargs):
        user = info.context.user
        chat = Chat.objects.prefetch_related("messages", "participants").get(participants=UserProfile.objects.get(user=user), id=id)
        return chat.messages.all()


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


class SendOtpVerification(Mutation):
    id = ID()
    class Arguments:
        email = String(required=True)
    @staticmethod
    def mutate(_, info, email):
        secret_code, hotp_at = send_otp_code(email, int(time.time()))        
        otp = OTPVerification( 
            secret = secret_code,
            hotp = hotp_at
        ) 
        otp.save()
        return SendOtpVerification( id=otp.id )   
        

class GetOtpVerification(Mutation):
    msg = String()
    class Arguments:
        otp_id = Int()
        code  = String()
    @staticmethod
    def mutate(_, info, otp_id,code):
        otp = OTPVerification.objects.get(id=otp_id)
        bl = check_otp_code(otp.secret, otp.hotp, code) 

        if bl == True:
            return GetOtpVerification(msg="Success") 
        else:
            return GetOtpVerification(msg="Failure")


        

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
            created_time = datetime.datetime.now()
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
        public_key = String(required = False)

    @staticmethod
    def mutate(_,  info, image, date_of_birth, phone_number, first_name, last_name, public_key): 
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
        if public_key is not None:
            usr_prof.public_key = public_key  
        
        
        usr_prof.save() 
        user.save() 

        return UpdateUserProfile(
                msg = "Succesful", 
                api_msg = apiMsg ) 


class CreateChat(Mutation):
    chat = Field(ChatType)
    error = String()

    class Arguments:
        user_id = ID (required=True) 
        name = String()
        key = String() 
    

    @staticmethod
    def mutate(_, info, user_id, name, key): 
        user = info.context.user   
        emails = str ( User.objects.get(id=user_id).email)
        emails = emails + f',{user.email}' 
        emails = emails.split(",")
        if len(emails) > 2:
            return CreateChat(error="you cannot have more then two participants if this is not a group")
        else:
            chat = Chat.objects.create(
                name=name, 
                key=key, 
                initiator = user.email, 
                state = 2
            )
            users = []
            for email in emails:
                kek = User.objects.get(email=email)
                usr = UserProfile.objects.get(user=kek)
                users.append(usr) 
                if email != user.email:
                    chat.acceptor = email
            chat.participants.add(*users) 
            chat.save()
    
        return CreateChat(chat=chat) 


class AcceptChat(Mutation):
    key = String()
    id = ID()

    class Arguments:
        chat_id = ID(required=True)
    
    @staticmethod
    def mutate(_, info, chat_id):  
        user = info.context.user  
        kek = UserProfile.objects.get(id=user.id)
        chat = Chat.objects.get(participants=kek, id=chat_id)
        chat.state = 1 
        chat.save()
        return AcceptChat(id = chat.id, key = chat.key) 

class DeclineChat(Mutation):
    msg = String() 

    class Arguments:
        chat_id = ID(required=True)
    @staticmethod
    def mutate(_, info, chat_id):  
        user = info.context.user  
        kek = UserProfile.objects.get(id=user.id)
        chat = Chat.objects.get(participants=kek, id=chat_id)
        chat.state = 0 
        chat.save()
        return DeclineChat(msg = f'declined from {user.email}')


class SendMessage(Mutation):
    message = Field(MessageType)

    class Arguments:
        message = String(required=True)
        chat_id = Int(required=True)

    @staticmethod
    def mutate(_, info, message, chat_id):
        user = info.context.user
        kek = UserProfile.objects.get(user=user)
        chat = Chat.objects.get(participants=kek, id=chat_id) 
        if chat.state == 1:
            message = Message.objects.create(
                sender= UserProfile.objects.get(user =user),
                text=message,
                created= datetime.datetime.now()
            )
            chat.messages.add(message)
            chat.save()
            return SendMessage(message=message)  
        else:
            return SendMessage(message=None)  




        
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

    create_chat = CreateChat.Field() 
    accept_chat = AcceptChat.Field()   
    decline_chat = DeclineChat.Field()
    send_message = SendMessage.Field() 

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

    send_otp_verification  = SendOtpVerification.Field() 
    get_otp_verification  = GetOtpVerification.Field()

    """
    Mutation Tags 
    """ 
    create_tags = CreateTags.Field() 







