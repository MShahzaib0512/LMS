from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',index , name="index"),
    path('application_form',application_form , name="application_form"),
    path('login_user',login_user , name="login_user"),
    path('logout_user',logout_user , name="logout_user"),
    path('register',register , name="register"),
    path('dashboard',dashboard , name="dashboard"),
    path('Application',Application , name="Application"),
    path('update_application',update_application , name="update_application"),
    path('view_users',view_users , name="view_users"),
    path('update_profile',update_profile , name="update_profile"),
    path('admin-dashboard', admin_dashboard, name='admin-dashboard'),
    path('admin-applications', admin_applictaions, name='admin-applications'),
    path('Approvals/<int:id>', Approvals, name='Approvals'),
    path('Rejections/<int:id>', Rejections, name='Rejections'),
    path('approved', approved, name='approved'),
    path('rejestion', rejestion, name='rejestion'),
    path('loan_products', loan_products, name='loan_products'),
    path('loan_calculator', loan_calculator, name='loan_calculator'),
    path('talk_to_expert', talk_to_expert, name='talk_to_expert'),
    path('aboutus', aboutus, name='aboutus'),
    path('contactus', contactus, name='contactus'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)