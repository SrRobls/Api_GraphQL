import graphene
from django.db import transaction
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from .models import UserApp_TB, UserDocument_TB, TypeDocument_TB, Country_TB, ContactInfo_TB
import bcrypt
import uuid
#GraphQL schema for UserApp_TB
class UserAppType(DjangoObjectType):
    class Meta:
        model = UserApp_TB
        fields = "__all__"

#GraphQL schema for UserDocument_TB
class UserDocumentType(DjangoObjectType):
    class Meta:
        model = UserDocument_TB
        fields = "__all__"

#GraphQL schema for TypeDocument_TB
class TypeDocumentType(DjangoObjectType):
    class Meta:
        model = TypeDocument_TB
        fields = "__all__"

#GraphQL schema for Country_TB
class CountryType(DjangoObjectType):
    class Meta:
        model = Country_TB
        fields = "__all__"

#GraphQL schema for ContactInfo_TB
class ContactInfoType(DjangoObjectType):
    class Meta:
        model = ContactInfo_TB
        fields = "__all__"


# Create the inputs for mutations

class UserDocumentInput(graphene.InputObjectType):
    document = graphene.String(required=True)
    name_type_document = graphene.String(required=True)
    place_expedition = graphene.String(required=True)
    date_expedition = graphene.Date(required=True)

class ContactInfoInput(graphene.InputObjectType):
    phone = graphene.String(required=True)
    cel_phone = graphene.String(required=True)
    address = graphene.String(required=True)
    city = graphene.String(required=True)
    country_name = graphene.String(required=True)
    emergency_name = graphene.String(required=True)
    emergency_phone = graphene.String(required=True)

class UserAppInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)
    name = graphene.String(required=True)
    lastname = graphene.String(required=True)
    is_militar = graphene.Boolean(required=False)
    is_temporal = graphene.Boolean(required=False)
    document = graphene.Argument(UserDocumentInput, required=True)
    contact = graphene.Argument(ContactInfoInput, required=True)


class UpdateUserFields(graphene.InputObjectType):
    email = graphene.String()
    name = graphene.String()
    lastname = graphene.String()
    is_militar = graphene.Boolean()
    is_temporal = graphene.Boolean()

class UpdateDocumentFields(graphene.InputObjectType):
    document = graphene.String()
    type_document_name = graphene.String()
    place_expedition = graphene.String()
    date_expedition = graphene.Date()

class UpdateContactFields(graphene.InputObjectType):
    phone = graphene.String()
    cel_phone = graphene.String()
    address = graphene.String()
    city = graphene.String()
    country_name = graphene.String()
    emergency_name = graphene.String()
    emergency_phone = graphene.String()



# Create de Base Query

class Query(graphene.ObjectType):
    all_users = graphene.List(UserAppType)
    all_user_documents = graphene.List(UserDocumentType)
    all_type_documents = graphene.List(TypeDocumentType)
    all_countries = graphene.List(CountryType)
    all_contact_info = graphene.List(ContactInfoType)
    user_by_id = graphene.Field(UserAppType, id=graphene.ID(required=True))
    user_by_email = graphene.Field(UserAppType, email=graphene.String(required=True))


    def resolve_all_users(self, info):
        users = UserApp_TB.objects.all()
        return users
    
    def resolve_all_user_documents(self, info):
        user_documents = UserDocument_TB.objects.all()
        return user_documents
    
    def resolve_all_type_documents(self, info):
        type_documents = TypeDocument_TB.objects.all()
        return type_documents
    
    def resolve_all_countries(self, info):
        countries = Country_TB.objects.all()
        return countries
    
    def resolve_all_contact_info(self, info):
        contact_info = ContactInfo_TB.objects.all()
        return contact_info
    
    def resolve_user_by_id(self, info, id):

        try:
            user = UserApp_TB.objects.get(pk=id)
            return user
        except Exception as e:
            return GraphQLError(f"User with id {id} not found: {str(e)}")
        
    def resolve_user_by_email(self, info, email):
        try:
            user = UserApp_TB.objects.get(email=email)
            return user
        except Exception as e:
            return GraphQLError(f"User with email {email} not found: {str(e)}")
    
    
# Create the mutations
# Create User Mutation
class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserAppInput(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserAppType)

    def mutate(self, info, input):
        try:
            with transaction.atomic():

                # Check if the username already exists
                if UserApp_TB.objects.filter(username=input.username).exists():
                    return CreateUser(success=False, message="Username already exists")
                
                # Check if the email already exists
                if UserApp_TB.objects.filter(email=input.email).exists():
                    return CreateUser(success=False, message="Email already exists")
                
                # Check if the document already exists
                if UserDocument_TB.objects.filter(document=input.document.document).exists():
                    return CreateUser(success=False, message="Document already exists")
                
                # Validate that the document number contains only numeric characters
                if not input.document.document.isdigit():
                    return CreateUser(success=False, message="Document number must contain only numeric characters")
                
                # Validate that the phone number contains only numeric characters
                if not input.contact.phone.isdigit():
                    return CreateUser(success=False, message="Phone number must contain only numeric characters")
                
                # Validate that the cellphone number contains only numeric characters
                if not input.contact.cel_phone.isdigit():
                    return CreateUser(success=False, message="Cellphone number must contain only numeric characters")
                
                # Validate that the emergency phone number contains only numeric characters
                if not input.contact.emergency_phone.isdigit():
                    return CreateUser(success=False, message="Emergency phone number must contain only numeric characters")
                
                try:
                    type_doc = TypeDocument_TB.objects.get(name_type_document__iexact=input.document.name_type_document)
                except TypeDocument_TB.DoesNotExist:
                    return CreateUser(success=False, message="Invalid type of Document")

                try:
                    country = Country_TB.objects.get(country_name__iexact=input.contact.country_name)
                except Country_TB.DoesNotExist:
                    return CreateUser(success=False, message="Invalid Country")
                
                # Hash the password
                hashed_password = bcrypt.hashpw(input.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                verification_token = str(uuid.uuid4())
                
                # Create the user
                user = UserApp_TB.objects.create(
                    username=input.username,
                    password=hashed_password,
                    email=input.email,
                    name=input.name,
                    last_name=input.lastname,
                    is_militar=input.is_militar or False, # Default to False if not provided
                    is_temporal=input.is_temporal or False, # Default to False if not provided
                    verification_token=verification_token,
                )   
            
                # Create the user document
                UserDocument_TB.objects.create(
                    user_id=user,
                    document=input.document.document,
                    type_document=type_doc,
                    place_expedition=input.document.place_expedition,
                    date_expedition=input.document.date_expedition
                )

                # Create the contact info
                ContactInfo_TB.objects.create(
                    user_id=user,
                    phone=input.contact.phone,
                    cel_phone=input.contact.cel_phone,
                    address=input.contact.address,
                    city=input.contact.city,
                    country_id=country,
                    emergency_name=input.contact.emergency_name,
                    emergency_phone=input.contact.emergency_phone
                )


                return CreateUser(success=True, message="User created successfully", user=user)
        except Exception as e:  
            # Handle any exceptions that occur during the transaction
            return CreateUser(success=False, message=f"An error occurred: {str(e)}")
    
# Update User Mutation   
class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        user = UpdateUserFields(required=False)
        document = UpdateDocumentFields(required=False)
        contact = UpdateContactFields(required=False)

    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserAppType)

    def mutate(self, info, id, user=None, document=None, contact=None):
        try:
            with transaction.atomic():
                user_obj = UserApp_TB.objects.get(pk=id)
                if user:
                    if user.email:
                        if UserApp_TB.objects.filter(email=user.email).exclude(pk=user_obj.pk).exists():
                            return UpdateUser(success=False, message="Email already in use")
                        user_obj.email = user.email
                    if user.name:
                        user_obj.name = user.name
                    if user.lastname:
                        user_obj.last_name = user.lastname
                    if user.is_militar is not None:
                        user_obj.is_militar = user.is_militar
                    if user.is_temporal is not None:
                        user_obj.is_temporal = user.is_temporal
                    user_obj.save()

                if document:
                    doc_obj = getattr(user_obj, "userdocument_tb", None)
                    if doc_obj:
                        if document.document:
                            doc_obj.document = document.document
                        if document.place_expedition:
                            doc_obj.place_expedition = document.place_expedition
                        if document.date_expedition:
                            doc_obj.date_expedition = document.date_expedition
                        if document.type_document_name:
                            try:
                                type_doc = TypeDocument_TB.objects.get(name_type_document__iexact=document.type_document_name)
                                doc_obj.type_document = type_doc
                            except TypeDocument_TB.DoesNotExist:
                                return UpdateUser(success=False, message="Invalid document type")
                        doc_obj.save()

                if contact:
                    contact_obj = getattr(user_obj, "contact", None)
                    if contact_obj:
                        if contact.phone: contact_obj.phone = contact.phone
                        if contact.cel_phone: contact_obj.cel_phone = contact.cel_phone
                        if contact.address: contact_obj.address = contact.address
                        if contact.city: contact_obj.city = contact.city
                        if contact.emergency_name: contact_obj.emergency_name = contact.emergency_name
                        if contact.emergency_phone: contact_obj.emergency_phone = contact.emergency_phone
                        if contact.country_name:
                            try:
                                country = Country_TB.objects.get(country_name__iexact=contact.country_name)
                                contact_obj.country_id = country
                            except Country_TB.DoesNotExist:
                                return UpdateUser(success=False, message="Invalid country")
                        contact_obj.save()

                return UpdateUser(success=True, message="User updated successfully", user=user_obj)
        except Exception as e:
            # Handle any exceptions that occur during the transaction
            return UpdateUser(success=False, message=f"An error occurred: {str(e)}")


# Delete User Mutation
class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            user_obj = UserApp_TB.objects.get(pk=id)
            user_obj.delete()
            return DeleteUser(success=True, message="User deleted successfully")
        except UserApp_TB.DoesNotExist:
            return DeleteUser(success=False, message="User not found")
        except Exception as e:
            return DeleteUser(success=False, message=f"An error occurred: {str(e)}")

# Create the mutation class to handle all mutations
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()