"""hit_DBMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from hit_DBMS_app import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('db_handle/', views.db_handle),

    path('', views.IndexView.as_view()),
    path('index/', views.IndexView.as_view()),
    path('Department/listDepartment/', views.listDepartment),
    path('Department/createDepartment/', views.createDepartment),
    path('Department/deleteDepartment/', views.deleteDepartment),
    path('Department/updateDepartment/', views.updateDepartment),

    path('Student/listStudent/', views.listStudent),
    path('Student/createStudent/', views.createStudent),
    path('Student/deleteStudent/', views.deleteStudent),
    path('Student/queryScore/', views.queryScore),
    path('Student/queryPrize/', views.queryPrize),

    path('Lab/listLab/', views.listLab),
    path('Lab/createLab/', views.createLab),

    path('Paper/listPaper/', views.listPaper),
    path('Paper/createPaper/', views.createPaper),

    path('Teacher/listTeacher/', views.listTeacher),
    path('Teacher/createTeacher/', views.createTeacher),

    path('Score/listScore/', views.listScore),
    path('Score/createScore/', views.createScore),
    path('Score/averageScore/', views.averageScore),

    path('Prize/listPrize/', views.listPrize),
    path('Prize/createPrize/', views.createPrize),

    path('Experience/listExperience/', views.listExperience),
    path('Experience/createExperience/', views.createExperience),
]


