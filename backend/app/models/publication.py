from app import db


class Publication(db.Model):
    __tablename__ = "publications"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    pub_type = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    region_id = db.Column(
        db.Integer,
        db.ForeignKey("regions.id"),
        nullable=True,
    )
    region = db.relationship("Region", backref="publications")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "pub_type": self.pub_type,
            "year": self.year,
            "description": self.description,
            "region_id": self.region_id,
            "author_ids": [
                author.id for author in self.authors
            ]
            if hasattr(self, "authors")
            else [],
        }
