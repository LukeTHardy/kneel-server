import json
import time
from nss_handler import status
from repository import db_get_single, db_get_all, db_create, db_delete

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

        if expanded_resources:
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

        if expanded_resources:
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

    def create(self, handler, request_body_data):
        current_timestamp = int(time.time())
        sql = """
        INSERT INTO ORDERS (timestamp, metalId, sizeId, styleId)
        VALUES (?, ?, ?, ?)
        """
        db_new_id = db_create(
            sql, (current_timestamp, request_body_data['metalId'], request_body_data['sizeId'], request_body_data['styleId']))

        if db_new_id:
            response_data = {
                "id": db_new_id,
                "timestamp": current_timestamp,
                "metalId": request_body_data['metalId'],
                "sizeId": request_body_data['sizeId'],
                "styleId": request_body_data['styleId']
            }
            return handler.response(json.dumps(response_data), status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return handler.response("Failed to create order", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        
    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM Orders WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)