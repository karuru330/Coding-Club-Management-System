from django.shortcuts import render,redirect
from ccms.models import Leaderboard
from django.core.mail import EmailMessage
def index(request):
	try:
		user = request.session['username']
		if request.session['type'] == "student":
			return redirect("/student_home")
		elif request.session['type'] == "cctm":
			return redirect("/cctm_home")
	except:
		pass
	message = ""
	user = None
	try:
		user = request.session['user']
		if user == "student":
			try:
				message = request.session['student_message']
				user = request.session['user']
				del request.session['student_message']
			except:
				message = ""
		elif user == "cctm":	
			try:
				message = request.session['cctm_message']
				user = request.session['user']
				del request.session['cctm_message']
			except:
				message = ""
		del request.session['user']
	except:
		pass
	return render(request,"index.html",{'message':message,'user':user})

def get_Leaderboard(request):
	leaderboard = Leaderboard.objects.all().order_by('-rating')
	i = 1
	for row in leaderboard:
		row.sno = i
		i = i+1
	return render(request,"leaderboard.html",{'leaderboard':leaderboard})
def sendemail(request):
	email = EmailMessage('Hi', 'CCMS', to=['dilli141330@gmail.com'])
	email.send()
# Create your views here.
