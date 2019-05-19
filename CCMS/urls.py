"""CCMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from ccms import studentViews
from ccms import cctmViews
from ccms import views

urlpatterns = [
	path('admin/', admin.site.urls),
 	path('index/', views.index),
	path('student_login', studentViews.student_login),
	path('student_home', studentViews.student_home),
	path('student_logout', studentViews.student_logout),
	path('cctm_login', cctmViews.cctm_login),
	path('cctm_home', cctmViews.cctm_home),
	path('cctm_logout', cctmViews.cctm_logout),
	path('manage_compete', cctmViews.manage_compete),
	path('campus_contests', cctmViews.campus_contests),
	path('online_contests', cctmViews.online_contests),
	path('create_campus_contest', cctmViews.create_campus_contest),
	path('manage_accounts', cctmViews.manage_accounts),
	path('add_member', cctmViews.add_member),
	path('remove_member/<str:username>', cctmViews.remove_member),
	path('add_online_contest', cctmViews.add_online_contest),
	path('edit_online_contest/<int:id>', cctmViews.edit_online_contest),
	path('update_online_contest/<int:id>', cctmViews.update_online_contest),
	path('delete_online_contest/<int:id>', cctmViews.delete_online_contest),
	path('manage_challenges', cctmViews.manage_challenges),
	path('create_challenge', cctmViews.create_challenge),
	path('edit_challenge/<str:challenge_name>', cctmViews.edit_challenge),
	path('edit_campus_contest/<str:contest_name>', cctmViews.edit_campus_contest),
	path('update_challenge/<str:challenge_name>', cctmViews.update_challenge),
	path('update_campus_contest/<str:contest_name>', cctmViews.update_campus_contest),
	path('modify_challenge/<str:contest_name>/<str:challenge_name>', cctmViews.modify_challenge),
	path('editorial/<str:challenge_name>', cctmViews.update_editorial),
	path('add_testcase/<str:challenge_name>', cctmViews.add_testcase),
	path('update_testcase/<str:challenge_name>/<int:id>', cctmViews.update_testcase),
	path('delete_testcase/<str:challenge_name>/<int:id>', cctmViews.delete_testcase),
	path('add_challenge/<str:contest_name>', cctmViews.add_challenge),
	path('remove_challenge/<str:contest_name>/<str:challenge_name>', cctmViews.remove_challenge),
	path('add_participant/<str:contest_name>', cctmViews.add_participant),
	path('add_all/<str:contest_name>', cctmViews.add_all),
	path('remove_participant/<str:contest_name>/<str:username>', cctmViews.remove_participant),
	path('send_notification/<str:contest_name>', cctmViews.send_notification),
	path('update_languages/<str:challenge_name>', cctmViews.update_languages),
	path('delete_campus_contest/<int:id>', cctmViews.delete_campus_contest),
	path('delete_challenge/<int:id>', cctmViews.delete_challenge),
	path('compete', studentViews.compete),
	path('compete/campus_contests', studentViews.campus_contests),
	path('compete/online_contests', studentViews.online_contests),
	path('compete/contests/<str:contest_name>', studentViews.contest_home),
	path('notifications', studentViews.notifications),
	path('compete/contests/<str:contest_name>/challenges', studentViews.contest_page),
	path('compete/contests/<str:contest_name>/challenges/<str:challenge_name>/problem_statement', studentViews.challenge_info),
	path('compete/contests/<str:contest_name>/challenges/<str:challenge_name>/submissions', studentViews.get_submissions),
	path('compete/contests/<str:contest_name>/challenges/<str:challenge_name>/leaderboard', studentViews.get_challenges_leaderboard),
	path('compete/contests/<str:contest_name>/challenges/<str:challenge_name>/editorial', studentViews.get_editorial),
	path('not_allowed_page', studentViews.not_allowed),
	path('submit/<str:contest_name>/<str:challenge_name>', studentViews.submit),
	path('run/<str:contest_name>/<str:challenge_name>', studentViews.run),
	path('contest_leaderboard/<str:contest_name>',studentViews.get_contest_leaderboard),
	path('leader_board',views.get_Leaderboard),
	path('email',views.sendemail),
]
