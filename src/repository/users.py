from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource
# from src.model.userModel import UserModel

class UserRepository:
    def __init__(self, db: ServiceResource) -> None:
        self.__db = db          # db resource will be injected when this repository is created in the main.py

    def get_all(self):
        table = self.__db.Table('UserDetails')  # referencing to table Recipes
        response = table.scan()             # scan all data
        return response.get('Items', [])    # return data

    def get_user(self,uid: str):
        try:
            table = self.__db.Table('UserDetails')          # referencing to table Recipes
            response = table.get_item(Key={'uid': uid})     # get recipe using uid (partition key)
            return response['Item']                         # return single data
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])

    def create_user(self,userdetails):
        table = self.__db.Table('UserDetails')      # referencing to table Recipes
        user = userdetails.dict()
        response = table.put_item(Item=user)  # create recipe
        return response                         # return response from dynamodb
    
    # def update_user(self, user: dict):
    #     table = self.__db.Table('UserDetails')      # referencing to table Recipes
    #     response = table.update_item(           # update single item
    #         Key={'uid': user.get('uid')},     # using partition key specifying which attributes will get updated
    #         UpdateExpression="""                
    #             set
    #                 author=:author,
    #                 description=:description,
    #                 ingredients=:ingredients,
    #                 title=:title,
    #                 steps=:steps
    #         """,
    #         ExpressionAttributeValues={         # values defined in here will get injected to update expression
    #             ':author': user.get('author'),
    #             ':description': user.get('description'),
    #             ':ingredients': user.get('ingredients'),
    #             ':title': user.get('title'),
    #             ':steps': user.get('steps')
    #         },
    #         ReturnValues="UPDATED_NEW"          # return the newly updated data point
    #     )
    #     return response

    def delete_user(self,uid: str):
        table = self.__db.Table('UserDetails')      # referencing to table Recipes
        response = table.delete_item(           # delete recipe using uuid
            Key={'uid': uid}
        )
        return response