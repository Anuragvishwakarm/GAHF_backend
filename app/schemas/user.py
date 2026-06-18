from pydantic import BaseModel

class UpdateProfileRequest(BaseModel):
    full_name:str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str