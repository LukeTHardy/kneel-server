import json
from nss_handler import status
from repository import db_get_single, db_get_all
# db_delete, db_update, db_create

class StylesView():
    
    def get(self, handler, pk):
        if pk != 0:
            style = self.get_single_style(pk)
            return handler.response(json.dumps(style), status.HTTP_200_SUCCESS.value)
        else:
            styles = self.get_all_styles()
            return handler.response(json.dumps(styles), status.HTTP_200_SUCCESS.value)
        
    def get_single_style(self, pk):
        sql = "SELECT s.id, s.style, s.price FROM Styles s WHERE s.id = ?"
        query_results = db_get_single(sql, pk)
        style = dict(query_results)

        return style
        
    def get_all_styles(self):
        sql = "SELECT s.id, s.style, s.price FROM Styles s"
        query_results = db_get_all(sql)
        styles = [dict(row) for row in query_results]

        return styles    