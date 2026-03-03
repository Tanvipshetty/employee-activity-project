from django.urls import path
from . import views

urlpatterns = [

    # ================= LOGIN =================
    path('', views.login_view, name='login'),

    # ================= EMPLOYEE =================
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('report/<int:id>/', views.report_detail, name='report_detail'),  # 👈 ADD THIS
    path('my-reports/', views.my_reports, name='my_reports'),

    # ================= GROUP HEAD =================
    path('gh-dashboard/', views.gh_dashboard, name='gh_dashboard'),
    path('gh-approve/<int:id>/', views.gh_approve, name='gh_approve'),
    path('gh-reject/<int:id>/', views.gh_reject, name='gh_reject'),

    # ================= HR =================
    path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('hr-approve/<int:id>/', views.hr_approve, name='hr_approve'),
    path('hr-reject/<int:id>/', views.hr_reject, name='hr_reject'),

    # ================= LOGOUT =================
    path('logout/', views.logout_view, name='logout'),
]