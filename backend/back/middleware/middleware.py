from django.http import HttpResponseNotFound

class FaviconMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/favicon.ico':
            return HttpResponseNotFound()
        return self.get_response(request)
