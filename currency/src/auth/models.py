from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from currency.db.base_model import Model


class User(Model):
    """ User model """
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    hash_password = Column(String(128), info={
        "verbose_name": "Password пользователя"
    })
    joined_date = Column(
        DateTime(timezone=True),
        server_default=func.now(), info={
            "verbose_name": "Дата когда пользователь зарег."
    })

    def __repr__(self):
        return f"id:{self.id} email: {self.email}"
