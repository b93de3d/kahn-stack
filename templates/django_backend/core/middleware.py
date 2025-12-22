from django.http import HttpResponse
from _KAHN_PROJECT_SLUG_.settings import GIT_VERSION


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/up":
            if self._is_app_really_healthy():
                response = HttpResponse(
                    f"_KAHN_PROJECT_NAME_ Reconciliation API is Healthy: {GIT_VERSION}"
                )
            else:
                response = HttpResponse(
                    f"_KAHN_PROJECT_NAME_ Reconciliation API is Down: {GIT_VERSION}", status=500
                )
        else:
            response = self.get_response(request)

        return response

    def _is_app_really_healthy(self):
        # TODO: Check db connections
        return True
