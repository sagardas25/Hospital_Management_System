from django.utils.deprecation import MiddlewareMixin



# class NoCacheMiddleware(MiddlewareMixin):
#     def process_response(self, request, response):
#         # Check if the request path is either /login/ or /register/
#         if request.path in ['/login/', '/register/' ,'/add_availability/']:
#             # Set headers to prevent caching
#             response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#             response['Pragma'] = 'no-cache'
#             response['Expires'] = '0'
#         return response
