import json
from nss_handler import status
from repository import db_get_single, db_get_all
# , db_delete, db_update, db_create

class OrdersView():
    
    def get(self, handler, pk):
        url = handler.parse_url(handler.path)

        if pk != 0:
            order = self.get_single_order(pk, url.get("_expand"))
            return handler.response(json.dumps(order), status.HTTP_200_SUCCESS.value)
        else:
            orders = self.get_all_orders(url.get("_expand"))
            return handler.response(json.dumps(orders), status.HTTP_200_SUCCESS.value)
        
    def get_single_order(self, pk, expanded_resources):
        sql = "SELECT o.id, o.timestamp, o.metalId, o.sizeId, o.styleId FROM Orders o WHERE o.id = ?"
        query_results = db_get_single(sql, pk)
        order = dict(query_results)

        for resource in expanded_resources:
            if resource == 'metal':
                self.get_expanded_metal_info(order)
            if resource == 'size':
                self.get_expanded_size_info(order)
            if resource == 'style':
                self.get_expanded_style_info(order)

        return order
        
    def get_all_orders(self, expanded_resources):
        sql = "SELECT o.id, o.timestamp, o.metalId, o.sizeId, o.styleId FROM Orders o"
        query_results = db_get_all(sql)
        orders = [dict(row) for row in query_results]

        for resource in expanded_resources:
            if resource == 'metal':
                for order in orders:
                    self.get_expanded_metal_info(order)
            if resource == 'size':
                for order in orders:
                    self.get_expanded_size_info(order)
            if resource == 'style':
                for order in orders:
                    self.get_expanded_style_info(order)

        return orders    

    def get_expanded_metal_info(self, order):
        metal_id = order.get('metalId')
        if metal_id != 0:
            metal_sql = "SELECT m.id, m.metal, m.price FROM Metals m WHERE m.id = ?"
            metal_info = db_get_single(metal_sql, metal_id)
            order['metal'] = dict(metal_info)
    def get_expanded_size_info(self, order):
        size_id = order.get('sizeId')
        if size_id != 0:
            size_sql = "SELECT s.id, s.carets, s.price FROM Sizes s WHERE s.id = ?"
            size_info = db_get_single(size_sql, size_id)
            order['size'] = dict(size_info)
    def get_expanded_style_info(self, order):
        style_id = order.get('styleId')
        if style_id != 0:
            style_sql = "SELECT s.id, s.style, s.price FROM Styles s WHERE s.id = ?"
            style_info = db_get_single(style_sql, style_id)
            order['style'] = dict(style_info)