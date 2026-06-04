from app import db


publication_authors = db.Table(
    "publication_authors",
    db.Column("publication_id", db.Integer, db.ForeignKey("publications.id")),
    db.Column("author_id", db.Integer, db.ForeignKey("authors.id")),
)


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    publications = db.relationship(
        "Publication", secondary=publication_authors, backref="authors"
    )
