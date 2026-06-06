from flask_restx import Api


def register_routes(api: Api):
    from app.routes.regions import ns as regions_ns
    from app.routes.publications import ns as publications_ns
    from app.routes.authors import ns as authors_ns
    from app.routes.pages import ns as pages_ns

    api.add_namespace(regions_ns, path="/regions")
    api.add_namespace(publications_ns, path="/publications")
    api.add_namespace(authors_ns, path="/authors")
    api.add_namespace(pages_ns, path="/pages")
