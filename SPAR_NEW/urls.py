from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views.client_viewset import *
from app.views.job_viewset import *
from app.views.activity_log_viewset import *
from app.views.login_viewset import *
from app.views.address_viewset import *
from app.views.chain_viewset import *
from app.views.employee_viewset import *
from app.views.extra_viewset import *
from app.views.product_viewset import *
from app.views.question_viewset import *
from app.views.store_viewset import *
from app.views.task_viewset import *
from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_swagger.views import get_swagger_view
# from django.conf.urls import url

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for your project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
    # security=[{'Token': []}] 
)

router = DefaultRouter()
router.register('state', StateViewSet, basename='state')
router.register('city', CityViewSet, basename='city')
router.register('user-client-address', UserClientAddressViewSet, basename='user-client-address')
router.register('pincode', PincodeViewSet, basename='pincode')
router.register('user-client', UserClientViewSet, basename='user-client')
router.register('user', UserViewSet, basename='user')
router.register('chain',ChainViewSet,basename='chain')
router.register('chain-store',ChainStoreViewSet,basename='chain-store')
router.register('job', JobViewSet, basename='job')
router.register('job-frequency', JobFrequencyViewSet, basename='job-frequency')
router.register('activity-log', ActivityLogViewSet, basename='activity-log')
router.register('user-employee', UserEmployeeViewSet, basename='user-employee')
router.register('department', DepartmentViewSet, basename='department')
router.register('organization', OrganizationViewSet, basename='organization')
router.register('product', ProductViewSet, basename='product')
router.register('product-media', ProductMediaViewSet, basename='product-media')
router.register('question', QuestionViewSet, basename='question')
router.register('question-group', QuestionGroupViewSet, basename='question-group')
router.register('store', StoreViewSet, basename='store')
router.register('store-media', StoreMediaViewSet, basename='store-media')
router.register('store-product', StoreProductViewSet, basename='store-product')
router.register('task', TaskViewSet, basename='task')
router.register('task-info', TaskInfoViewSet, basename='task-info')
router.register('roles', RoleViewSet, basename='roles')

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='login'),
    path('token-refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    path('states/<int:state_id>/cities/', CityViewSet.as_view({'get': 'get'}), name='state-cities'),
    path('client-address/', ClientAddressViewSet.as_view(), name='client-address-list'),
    path('client-excel/', ClientExcel.as_view(), name='client-excel'),
    path('employee-excel/', EmployeeExcel.as_view(), name='client-excel'),
    path('client-address/<int:pk>/', ClientAddressViewSet.as_view(), name='client-address-detail'),
    path('store-address/', StoreAddressViewSet.as_view(), name='store-address-list'),
    path('store-address/<int:pk>/', StoreAddressViewSet.as_view(), name='store-address-detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
