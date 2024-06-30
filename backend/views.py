# views.py

from django.http import JsonResponse


def api_root(request):
    """
    API root endpoint.

    Returns a JSON response with a welcome message and status code 200.

    """
    return JsonResponse(
        {
            "status": 200,
            "message": "Welcome to Socialvibe Django REST Framework API"}
    )
