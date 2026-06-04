from app import db


class Publication(db.Model):
    __tablename__ = "publications"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    pub_type = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    region_id = db.Column(db.Integer, db.ForeignKey("regions.id"), nullable=True)
    region = db.relationship("Region", backref="publications")
