class InterfaceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        mode = request.GET.get("ui")
        if mode in ("classic", "tabler"):
            request.session["interface_mode"] = mode
        request.interface_mode = request.session.get("interface_mode", "tabler")
        return self.get_response(request)
