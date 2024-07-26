import uuid
from app.models import EmailSendRecord


class TrackService:
    def get_user_id_by_tracking_id(self, tracking_id):
        instance = EmailSendRecord.query.filter(EmailSendRecord.tracking_id == tracking_id).first()
        return instance.user_id if instance else None

    def generate_tracking_id(self):
        return uuid.uuid4().hex


track_service = TrackService()
