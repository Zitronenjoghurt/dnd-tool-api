from pydantic import BaseModel

class MessageResponse(BaseModel):
    message: str

    @staticmethod
    def create(message: str) -> 'MessageResponse':
        return MessageResponse(message=message)