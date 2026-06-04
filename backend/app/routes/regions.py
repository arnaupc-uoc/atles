from flask_restx import Namespace, Resource

ns = Namespace("regions", description="Region operations")


@ns.route("/")
class RegionList(Resource):
    def get(self):
        return {"message": "Not implemented yet"}

    def post(self):
        return {"message": "Not implemented yet"}


@ns.route("/<int:id>")
class RegionDetail(Resource):
    def get(self, id):
        return {"message": "Not implemented yet"}

    def put(self, id):
        return {"message": "Not implemented yet"}

    def delete(self, id):
        return {"message": "Not implemented yet"}
