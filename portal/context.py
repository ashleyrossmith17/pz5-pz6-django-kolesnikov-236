def portal_context(request):
    profile = getattr(request.user, "profile", None) if request.user.is_authenticated else None
    return {
        "interface_mode": getattr(request, "interface_mode", "tabler"),
        "can_manage": request.user.is_authenticated and (request.user.is_staff or (profile and profile.role in ("admin", "methodist"))),
    }
