# Add your imports below this line

import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
from views import OrdersView, SizesView, StylesView, MetalsView


class JSONServer(HandleRequests):

    def do_GET(self):
        url = self.parse_url(self.path)
        view = self.determine_view(url)

        try:
            view.get(self, url["pk"])
        except AttributeError:
            return self.response("No view for that route", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_PUT(self):
        url = self.parse_url(self.path)
        view = self.determine_view(url)
        return self.response("Unsupported method", status.HTTP_405_UNSUPPORTED_METHOD.value)

    def do_POST(self):
        # Parse the URL
        url = self.parse_url(self.path)
        # Determine the correct view needed to handle the requests
        view = self.determine_view(url)
        # Get the request body
        request_body = self.get_request_body()
        # if request_body.len() < 3:
        #     return self.response("Bad request data", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)
        try:
            view.create(self, request_body)
        # Make sure you handle the AttributeError in case the client requested a route that you don't support
        except AttributeError:
            return self.response("Unsupported method on this resource", status.HTTP_405_UNSUPPORTED_METHOD.value)


    def do_DELETE(self):
        url = self.parse_url(self.path)
        view = self.determine_view(url)

        try:
            view.delete(self, url["pk"])
        except AttributeError:
            return self.response("Unsupported method", status.HTTP_405_UNSUPPORTED_METHOD.value)

    def determine_view(self, url):
        """Lookup the correct view class to handle the requested route

        Args:
            url (dict): The URL dictionary

        Returns:
            Any: An instance of the matching view class
        """
        try:
            routes = {
                "orders": OrdersView,
                "sizes": SizesView,
                "styles": StylesView,
                "metals": MetalsView,
            }

            matching_class = routes[url["requested_resource"]]
            return matching_class()
        except KeyError:
            return status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ''
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
