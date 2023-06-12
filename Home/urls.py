from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path("", views.index, name="HOME"),
    path("course", views.Course, name="course"),
    path("library", views.library_view, name="library"),
    path("book_allocate", views.library_view, name="book_allocate"),
    path("attendance", views.attendance, name="attendance"),
    path("enrollment", views.Enrollment, name="enrollment"),
    path("finance", views.Finance, name="finance"),
    path('update-fees/<int:student_id>/', views.update_fees, name='update_fees'),
    path("placement", views.Placement, name="placement"),
    path("student", views.student, name="student"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
