from datetime import datetime

from app import db


class AccessLog(db.Model):
    __tablename__ = "access_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    username = db.Column(db.String(80), nullable=True)
    ip = db.Column(db.String(45), nullable=True)
    action = db.Column(db.String(80), nullable=False)
    success = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.username,
            "ip": self.ip,
            "action": self.action,
            "success": self.success,
            "created_at": self.created_at.isoformat(),
        }
