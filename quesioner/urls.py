"""quesioner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from jurica import views as jurica

urlpatterns = [
    url(r'^$', jurica.information, name='informasi'),
    url(r'^mendaftar/', jurica.register, name='mendaftar'),
    url(r'^masukadmin/?', jurica.loginadmin, name='masukadmin'),
    url(r'^masuk/?', jurica.login, name='masuk'),
    url(r'^keluaradmin/', jurica.logoutadmin, name='keluaradmin'),
    url(r'^keluar/', jurica.logout, name='keluar'),
    url(r'^selesai/', jurica.finish, name='selesai'),
    url(r'^pertanyaan/?', jurica.questionnaire, name='pertanyaan'),
    url(r'^mulaimengerjakan/', jurica.start, name='mulaimengerjakan'),
    url(r'^admin/responden/', jurica.responden, name='responden'),
    url(r'^admin/tambahresponden/', jurica.addresponden, name='tambahresponden'),
    url(r'^admin/ubahresponden/$', jurica.editresponden, name='ubahresponden'),
    url(r'^admin/hapusresponden/$', jurica.removeresponden, name='hapusresponden'),
    url(r'^admin/resetresponden/$', jurica.resetresponden, name='resetresponden'),
    url(r'^admin/detailresponden/$', jurica.detailresponden, name='detailresponden'),
    url(r'^admin/', jurica.admin, name='admin'),
    url(r'^ajax/table_responden/', jurica.table_responden, name='table_responden'),
]
