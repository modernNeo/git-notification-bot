class LogErrorResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        content = getattr(response, 'content', b'').decode('utf-8', errors='ignore')
        print(f"\n[!]. Response {response.status_code} for {request.path}")
        print(f"Content: {content}\n")

        return response
