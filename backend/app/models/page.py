from app import db


class Page(db.Model):
    __tablename__ = "pages"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=True)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
    )
    updated_at = db.Column(
        db.DateTime,
        onupdate=db.func.now(),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "published": self.published,
            "created_at":
            self.created_at.isoformat()
            if self.created_at
            else None,
            "updated_at":
            self.updated_at.isoformat()
            if self.updated_at
            else None,
        }
