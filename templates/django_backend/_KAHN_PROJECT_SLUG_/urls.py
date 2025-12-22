from django.urls import include, path
import core.views as core_views
from tools.dynamic_rest.routers import DynamicRouter

router = DynamicRouter()
router.register("users", core_views.UserViewSet)
router.register("user_profiles", core_views.UserProfileViewSet)
router.register("examples", core_views.ExampleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("csrf", core_views.csrf),
    path("version", core_views.version),
    path("accounts/", include("allauth.urls")),
    path("_allauth/", include("allauth.headless.urls")),
]
