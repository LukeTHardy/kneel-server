import json
from nss_handler import status
from repository import db_get_single, db_get_all 
# db_delete, db_update, db_create

class SizesView():
    
    def get(self, handler, pk):
        if pk != 0:
            size = self.get_single_size(pk)
            return handler.response(json.dumps(size), status.HTTP_200_SUCCESS.value)
        else:
            sizes = self.get_all_sizes()
            return handler.response(json.dumps(sizes), status.HTTP_200_SUCCESS.value)
        
    def get_single_size(self, pk):
        sql = "SELECT s.id, s.carets, s.price FROM Sizes s WHERE s.id = ?"
        query_results = db_get_single(sql, pk)
        size = dict(query_results)

        return size
        
    def get_all_sizes(self):
        sql = "SELECT s.id, s.carets, s.price FROM Sizes s"
        query_results = db_get_all(sql)
        sizes = [dict(row) for row in query_results]

        return sizes    