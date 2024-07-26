from .exts import marshmallow, db
from .models import UserEvent


class UserEventSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = UserEvent
        load_instance = True
        session = db.session
