from fastapi import APIRouter
from fastapi import HTTPException

from src.model.userModel import UserModel
from src.repository.users import UserRepository


class UsersRouter:
    def __init__(self, userRepository: UserRepository) -> None:
        self.__userRepository = userRepository
    @property
    def router(self):
        api_router = APIRouter(prefix='/users', tags=['users'])

        @api_router.get('/')
        def index_route():
            return {"greeting":"Welcome to Cloud Architecture Module"}
        
        @api_router.get('/all')
        def get_all():
            return self.__userRepository.get_all()
        
        @api_router.post('/create')
        def create_user(userdetails: UserModel):
            return self.__userRepository.create_user(userdetails)


        return api_router