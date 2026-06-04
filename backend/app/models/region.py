from app import db
from geoalchemy2 import Geometry


class Region(db.Model):
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    region_type = db.Column(db.String(50), nullable=False)
    geometry = db.Column(Geometry(geometry_type="MULTIPOLYGON", srid=4326))
    parent_id = db.Column(db.Integer, db.ForeignKey("regions.id"), nullable=True)
    parent = db.relationship("Region", remote_side="Region.id", backref="children")
