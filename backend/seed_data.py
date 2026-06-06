#!/usr/bin/env python3
import gzip
import os
import random
import subprocess
import string
from datetime import datetime

from geoalchemy2 import WKTElement

from app import create_app, db
from app.models import Author, Page, Publication, Region, User
from app.models.author import publication_authors

REGION_TYPES = ["municipi", "comarca", "província", "regió", "districte"]
PUBLICATION_TYPES = ["llibre", "documental", "pel·lícula", "article", "reportatge"]
USER_FIRST_NAMES = [
    "marta",
    "laura",
    "joan",
    "pau",
    "roser",
    "nuria",
    "jordi",
    "sara",
    "nil",
    "anna",
    "mireia",
    "ricard",
    "nina",
    "pol",
    "eva",
]
PAGE_TITLES = [
    "Inici",
    "Contacte",
    "Sobre nosaltres",
    "Notícies",
    "Serveis",
    "Ajuda",
    "Política de privacitat",
    "Termes d'ús",
    "Blog",
    "Projecte",
    "Mapa",
    "Equip",
]
REGION_NAMES = [
    "Cap de Creus",
    "Berguedà",
    "Garrotxa",
    "Penedès",
    "Alt Empordà",
    "Baix Llobregat",
    "Vallès Oriental",
    "La Selva",
    "Montsià",
    "Urgell",
    "Segarra",
    "Garraf",
    "Osona",
    "Anoia",
    "Ripollès",
]
AUTHOR_NAMES = [
    "Marc Vidal",
    "Clara Soler",
    "Pere Ribas",
    "Aina Puig",
    "Oriol Serra",
    "Laia Farré",
    "Nil Vives",
    "Júlia Bosch",
    "Francesc Miró",
    "Núria Costa",
    "Roger Rius",
    "Sílvia Oliver",
    "Biel Ferrer",
    "Helena Giralt",
    "Lluc Pujol",
]


def random_word(length=5):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def random_sentence(min_words=5, max_words=12):
    count = random.randint(min_words, max_words)
    return " ".join(random_word(random.randint(4, 9)) for _ in range(count)).capitalize() + "."


def random_slug(text):
    normalized = text.lower().replace(" ", "-")
    return "".join(ch for ch in normalized if ch.isalnum() or ch == "-")


def random_email(name):
    local = name.lower().replace(" ", ".")
    return f"{local}@example.com"


def random_geometry(index):
    base_lon = 1.0 + (index % 10) * 0.15
    base_lat = 41.0 + (index // 10) * 0.15
    coords = [
        (base_lon, base_lat),
        (base_lon + 0.08, base_lat),
        (base_lon + 0.08, base_lat + 0.08),
        (base_lon, base_lat + 0.08),
        (base_lon, base_lat),
    ]
    ring = ", ".join(f"{x} {y}" for x, y in coords)
    return WKTElement(f"MULTIPOLYGON((({ring})))", srid=4326)


def choose_random_item(source):
    return random.choice(source)


def build_database():
    app = create_app()
    with app.app_context():
        print("Creant esquema de la base de dades i assegurant admin...")
        db.create_all()

        admin_user = User.query.filter_by(username="admin").first()
        if not admin_user:
            admin_user = User(username="admin", email="admin@example.com")
            admin_user.set_password("admin")
            db.session.add(admin_user)
            db.session.commit()
            print("Usuari admin creat: admin / admin")
        else:
            admin_user.set_password("admin")
            admin_user.email = "admin@example.com"
            db.session.commit()
            print("Usuari admin actualitzat: admin / admin")

        print("Eliminant dades anteriors (excepte admin)...")
        db.session.execute(publication_authors.delete())
        Publication.query.delete()
        Author.query.delete()
        Page.query.delete()
        Region.query.delete()
        User.query.filter(User.username != "admin").delete()
        db.session.commit()

        user_count = random.randint(10, 20)
        region_count = random.randint(10, 20)
        author_count = random.randint(10, 20)
        publication_count = random.randint(10, 20)
        page_count = random.randint(10, 20)

        print(
            f"Creant {user_count} usuaris, {region_count} regions, {author_count} autors, "
            f"{publication_count} publicacions i {page_count} pàgines."
        )

        users = [admin_user]
        for i in range(1, user_count):
            name = random.choice(USER_FIRST_NAMES)
            username = f"{name}{i}"
            user = User(
                username=username,
                email=random_email(username),
            )
            user.set_password("password")
            users.append(user)
        db.session.add_all(users)

        regions = []
        for i in range(region_count):
            region_type = choose_random_item(REGION_TYPES)
            region_name = choose_random_item(REGION_NAMES)
            region = Region(
                name=f"{region_name} {i + 1}",
                region_type=region_type,
                geometry=random_geometry(i),
            )
            regions.append(region)
        db.session.add_all(regions)

        authors = []
        for i in range(author_count):
            author_name = choose_random_item(AUTHOR_NAMES)
            author = Author(
                name=f"{author_name} {i + 1}",
                bio=random_sentence(10, 25),
            )
            authors.append(author)
        db.session.add_all(authors)

        pages = []
        for i in range(page_count):
            title = choose_random_item(PAGE_TITLES)
            page = Page(
                title=f"{title} {i + 1}",
                slug=random_slug(f"{title}-{i + 1}"),
                content="\n\n".join(random_sentence(12, 20) for _ in range(5)),
                published=bool(random.getrandbits(1)),
            )
            pages.append(page)
        db.session.add_all(pages)

        db.session.commit()

        publications = []
        for i in range(publication_count):
            pub_type = choose_random_item(PUBLICATION_TYPES)
            title = f"{pub_type.capitalize()} {random_word(6).capitalize()} {i + 1}"
            publication = Publication(
                title=title,
                pub_type=pub_type,
                year=random.randint(1990, 2025),
                description=" ".join(random_sentence(8, 18) for _ in range(3)),
                region=random.choice(regions),
            )
            publication.authors = random.sample(authors, min(max(1, random.randint(1, 3)), len(authors)))
            publications.append(publication)
        db.session.add_all(publications)
        db.session.commit()

        print("Dades de prova generades correctament.")
        return app


def create_backup(app):
    backups_dir = app.config.get("BACKUPS_DIR")
    db_url = app.config.get("SQLALCHEMY_DATABASE_URI")
    pg_dump = app.config.get("PG_DUMP_PATH", "pg_dump")

    if not backups_dir or not db_url:
        raise RuntimeError("Falten configuració de BACKUPS_DIR o DATABASE_URL.")

    os.makedirs(backups_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_name = f"seed_backup_{timestamp}.sql.gz"
    out_path = os.path.join(backups_dir, out_name)

    print(f"Creant backup a {out_path}...")
    result = subprocess.run(
        [pg_dump, "--dbname", db_url],
        capture_output=True,
        timeout=300,
    )

    if result.returncode != 0:
        stderr = result.stderr.decode(errors="ignore")
        raise RuntimeError(f"pg_dump ha fallat: {stderr}")

    with gzip.open(out_path, "wb") as f:
        f.write(result.stdout)

    print(f"Backup creat correctament: {out_path}")
    return out_path


def main():
    app = build_database()
    backup_path = create_backup(app)
    print("Operació completada. Dataset i backup disponibles.")
    print(f"Fitxer de backup: {backup_path}")


if __name__ == "__main__":
    main()
