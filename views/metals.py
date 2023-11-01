import json
from nss_handler import status
from repository import db_get_single, db_get_all
# db_delete, db_update, db_create

class MetalsView():
    
    def get(self, handler, pk):
        if pk != 0:
            metal = self.get_single_metal(pk)
            return handler.response(json.dumps(metal), status.HTTP_200_SUCCESS.value)
        else:
            metals = self.get_all_metals()
            return handler.response(json.dumps(metals), status.HTTP_200_SUCCESS.value)
        
    def get_single_metal(self, pk):
        sql = "SELECT m.id, m.metal, m.price FROM Metals m WHERE m.id = ?"
        query_results = db_get_single(sql, pk)
        metal = dict(query_results)

        return metal
        
    def get_all_metals(self):
        sql = "SELECT m.id, m.metal, m.price FROM Metals m"
        query_results = db_get_all(sql)
        metals = [dict(row) for row in query_results]

        return metals    