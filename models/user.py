import uuid
from data_access.db_config import STATUS_PENDING, ROLE_MEMBER

class User:

    def __init__(self, name, password, role=ROLE_MEMBER,
                 status=STATUS_PENDING, user_id=None):
        self.__user_id  = user_id if user_id else str(uuid.uuid4())[:8].upper()
        self.__name     = name.strip()
        self.__password = password.strip()
        self.__role     = role
        self.__status   = status  # pending / verified / rejected

    # --- Getters ---
    @property
    def user_id(self):
        return self.__user_id

    @property
    def name(self):
        return self.__name

    @property
    def password(self):
        return self.__password

    @property
    def role(self):
        return self.__role

    @property
    def status(self):
        return self.__status

    # --- Setter sirf status ke liye --- admin approve/reject karega
    @status.setter
    def status(self, value):
        self.__status = value

    def is_verified(self):
        return self.__status == "verified"

    def is_admin(self):
        return self.__role == "admin"

    def to_dict(self):
        return {
            "user_id" : self.__user_id,
            "name"    : self.__name,
            "password": self.__password,
            "role"    : self.__role,
            "status"  : self.__status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name     = data["name"],
            password = data["password"],
            role     = data["role"],
            status   = data["status"],
            user_id  = data["user_id"]
        )

    def __str__(self):
        return f"[{self.__user_id}] {self.__name} | Role: {self.__role} | Status: {self.__status}"