from django.shortcuts import render,redirect
from django.http import HttpResponse
from ccms.forms import CCTMLogin, Create_Campus_Contest_Form,Create_Campus_ContestForm,CCTMForm,Online_Contest_Form, Create_Challenge_Form, Editorial,Member,TestcaseForm,TestcaseForm1,Contest_Challenges_Form,Participant_Form,Notification_Form
from ccms.models import CCTM,Online_Contest,Create_Challenge,Create_Campus_Contest,Student,Testcase,Contest_Challenges,Participant,Notification,Languages
import os
from datetime import date, datetime
import pytz
import shutil

from django.core.mail import EmailMessage
def send_email(mail_id,subject,message):
	email = EmailMessage(subject, message, to=[mail_id])
	email.send()

def check_user(request):
	try:
		username = request.session['username']
		Type = request.session['type']
		if(Type == "cctm"):
			return True
		elif(Type == "student"):
			return "student"
	except:
		return False
def cctm_login(request):
	username = ""
	password = ""
	clear_message_session(request)
	if(request.method == "POST"):
		MyLoginForm = CCTMLogin(request.POST)
		if(MyLoginForm.is_valid()):
			username = MyLoginForm.cleaned_data['username']
			password = MyLoginForm.cleaned_data['password']
			dbuser = CCTM.objects.filter(username=username,password=password)
			if not dbuser:
				request.session['cctm_message']="Incorrect username or password"
				request.session['user'] = 'cctm'
				return redirect("/index")
			request.session['username'] = username
			request.session['type'] = 'cctm'
			request.session['cctm_message'] = ""
			request.session['user'] = 'cctm'
			return redirect('/cctm_home')
		else:
			request.session['cctm_message'] = ""
			request.session['user'] = 'cctm'
			return redirect("/index")
def cctm_home(request):
	clear_message_session(request)
	try:
		if(request.session['username']!=None and request.session['type']=="cctm"):
			request.session['cctm_message'] = ""
			request.session['user'] = 'cctm'
			return render(request,"cctm_home.html")
		elif(request.session['username']!=None and request.session['type']=="student"):
			request.session['cctm_message'] = ""
			request.session['user'] = 'cctm'
			return redirect("/student_home")
		else:
			request.session['cctm_message']="You are not logged in .."
			request.session['user'] = 'cctm'
			return redirect("/index")
	except:
		request.session['cctm_message']="You are not logged in .."
		request.session['user'] = 'cctm'
		return redirect("/index")

def cctm_logout(request):
	clear_message_session(request)
	try:
		del request.session['username']
		del request.session['type']
	except:
		pass
	request.session['cctm_message']="You are successfully logged out .."
	request.session['user'] = 'cctm'
	return redirect("/index")
def manage_compete(request):
	if(check_user(request) == True):
		return redirect("/campus_contests")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def campus_contests(request):
	if(check_user(request) == True):
		message = ""
		try:
			message = request.session["message"]
			del request.session["message"]
		except:
			pass
		campus_contests = Create_Campus_Contest.objects.all()
		return render(request,"manage_compete.html",{'tab_status':'campus','campus_contests':campus_contests,'message':message})
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def online_contests(request):
	if(check_user(request) == True):
		message = ""
		try:
			message = request.session["message"]
			del request.session["message"]
		except:
			pass
		online_contests = Online_Contest.objects.all()
		return render(request,"manage_compete.html",{'tab_status':'online','online_contests':online_contests,'message':message})
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def create_campus_contest(request):
	if(check_user(request) == True):
		if request.method == "GET":
			return render(request,"create_campus_contest.html")
		elif request.method == "POST":
			MyForm = Create_Campus_Contest_Form(request.POST)
			if MyForm.is_valid():
				contest = Create_Campus_Contest.objects.filter(contest_name=MyForm.cleaned_data['contest_name'])
				if(not contest):
					Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Contests/"+MyForm.cleaned_data['contest_name']
					os.mkdir(Path)
					f1 = open(Path+"/description.txt","w")
					f1.write(MyForm.cleaned_data['description'])
					f1.close()
					f1 = open(Path+"/prizes.txt","w")
					f1.write(MyForm.cleaned_data['prizes'])
					f1.close()
					f1 = open(Path+"/rules.txt","w")
					f1.write(MyForm.cleaned_data['rules'])
					f1.close()
					f1 = open(Path+"/scoring.txt","w")
					f1.write(MyForm.cleaned_data['scoring'])
					f1.close()
					MyForm = Create_Campus_ContestForm(request.POST)
					MyForm.save()
					request.session['message']="campus contest "+str(MyForm.cleaned_data['contest_name'])+" created successfully"
				else:
					request.session['message']="campus contest "+str(MyForm.cleaned_data['contest_name'])+" Already Existed"
			return redirect("/manage_compete")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def edit_campus_contest(request,contest_name):
	if(check_user(request) == True):
		if request.method == "GET":
			campus_contest = Create_Campus_Contest.objects.get(contest_name=contest_name)
			Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Contests/"+contest_name+"/"
			f1 = open(Path+"description.txt","r")
			description = str(f1.read())
			f1.close()
			f1 = open(Path+"prizes.txt","r")
			prizes = str(f1.read())
			f1.close()
			f1 = open(Path+"rules.txt","r")
			rules = str(f1.read())
			f1.close()
			f1 = open(Path+"scoring.txt","r")
			scoring = str(f1.read())
			f1.close()
			challenges = Create_Challenge.objects.all()
			contest_challenges = Contest_Challenges.objects.filter(contest_name=contest_name)
			participants = Participant.objects.filter(contest_name=contest_name)
			return render(request,"edit_campus_contest.html",{'campus_contest':campus_contest,'prizes':prizes,'rules':rules,'scoring':scoring,'description':description,'challenges':challenges,'contest_challenges':contest_challenges,'participants':participants})
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")	
def update_campus_contest(request,contest_name):
	if(check_user(request) == True):
		campus_contest = Create_Campus_Contest.objects.get(contest_name=contest_name)
		MyForm = Create_Campus_ContestForm(request.POST,instance=campus_contest)
		MyForm.save()
		Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Contests/"+contest_name
		f1 = open(Path+"/description.txt","w")
		f1.write(MyForm.cleaned_data['description'])
		f1.close()
		f1 = open(Path+"/prizes.txt","w")
		f1.write(MyForm.cleaned_data['prizes'])
		f1.close()
		f1 = open(Path+"/rules.txt","w")
		f1.write(MyForm.cleaned_data['rules'])
		f1.close()
		f1 = open(Path+"/scoring.txt","w")
		f1.write(MyForm.cleaned_data['scoring'])
		f1.close()
		request.session['message']=contest_name+" updated successfully"
		return redirect("/manage_compete")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")

def add_challenge(request,contest_name):
	if(check_user(request) == True):
		Form = Contest_Challenges_Form(request.POST)
		if Form.is_valid():
			challenge = Contest_Challenges.objects.filter(contest_name=contest_name,challenge_name=Form.cleaned_data['challenge_name'])
			if not challenge:
				challenge_object = Create_Challenge.objects.get(challenge_name=Form.cleaned_data['challenge_name'])
				contest_object = Create_Campus_Contest.objects.get(contest_name=contest_name)
				challenge = Contest_Challenges()
				challenge.contest_name = contest_name
				challenge.challenge_name = Form.cleaned_data['challenge_name']
				challenge.challenge_id = challenge_object
				challenge.contest_id = contest_object
				challenge.score = int(Form.cleaned_data['score'])
				challenge.save()
				request.session['message']="challenge "+str(Form.cleaned_data['challenge_name'])+" added successfully"
			return redirect("/manage_compete")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")

def modify_challenge(request,contest_name,challenge_name):
	if(check_user(request) == True):
		Form = Contest_Challenges_Form(request.POST)
		if Form.is_valid():
			challenge = Contest_Challenges.objects.get(challenge_name=challenge_name,contest_name=contest_name)
			challenge.score = Form.cleaned_data['score']
			challenge.save()
			request.session['message']="challenge "+challenge_name+" modified successfully"
			return redirect("/manage_compete")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def remove_challenge(request,contest_name,challenge_name):
	if(check_user(request) == True):
		challenge = Contest_Challenges.objects.get(challenge_name=challenge_name,contest_name=contest_name)
		challenge.delete()
		request.session['message']="Challenge "+challenge_name+" "+" Successfully removed from"+contest_name
		return redirect("/manage_compete")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def add_participant(request,contest_name):
	if(check_user(request) == True):
		if request.method == "GET":
			message = ""
			try:
				message = request.session["message"]
				del request.session["message"]
			except:
				pass
			return render(request,"add_participant.html",{'contest_name':contest_name,'message':message})
		else:
			Form = Participant_Form(request.POST)
			if Form.is_valid():
				participant = Participant.objects.filter(username=Form.cleaned_data['username'],contest_name=contest_name)
				if participant:
					request.session['message']="Participant "+(Form.cleaned_data['username'])+" Already Existed"
					return redirect("/add_participant/"+contest_name)
				else:
					participant = Student.objects.filter(username=Form.cleaned_data['username'])
					if participant:
						participant = Participant()
						participant.username = Form.cleaned_data['username']
						participant.contest_name = contest_name
						contest_object = Create_Campus_Contest.objects.get(contest_name=contest_name)
						participant.contest_id = contest_object
						participant.save()
						request.session['message']="student "+str(Form.cleaned_data['username'])+" added as participant successfully to "+contest_name
						return redirect("/manage_compete")
					else:
						request.session['message']="participant "+str(Form.cleaned_data['username'])+" should be a student"
						return redirect("/add_participant/"+contest_name)
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def add_all(request,contest_name):
	if(check_user(request) == True):
		participant = Participant.objects.filter(contest_name=contest_name)
		for p in participant:
			p.delete()
		students = Student.objects.all()
		for student in students:
			participant = Participant()
			participant.username = student.username
			participant.contest_name =contest_name
			contest_object = Create_Campus_Contest.objects.get(contest_name=contest_name)
			participant.contest_id = contest_object
			participant.save()
		request.session['message']="all students added as participants successfully to "+contest_name
		return redirect("/manage_compete")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def remove_participant(request,contest_name,username):
	if(check_user(request) == True):
		participant = Participant.objects.get(username=username,contest_name=contest_name)
		participant.delete()
		request.session['message']="participant "+username+" removed successfully from "+contest_name
		return redirect("/manage_compete")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def send_notification(request,contest_name):
	if(check_user(request) == True):
		Form = Notification_Form(request.POST)
		if Form.is_valid():
			participants = Participant.objects.filter(contest_name=contest_name)
			tz = pytz.timezone('Asia/Kolkata')
			time = str(datetime.now(tz).time())
			time = time[0:8]
			for participant in participants:
				notification = Notification()
				notification.username = participant.username
				notification.contest_name =contest_name
				notification.date = date.today()
				notification.time = time
				notification.message = Form.cleaned_data['message']
				notification.save()
			request.session['message']="Notification sent successfully to all the participants of "+contest_name
			return redirect("/manage_compete")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def manage_accounts(request):
	if(check_user(request) == True):
		cctms = CCTM.objects.all()
		user = ""
		message = ""
		try:
			user = request.session['username']
			message = request.session['message']
			del request.session['message']
		except:
			pass
		return render(request,"manage_accounts.html",{'cctms':cctms,'user':user,'message':message})
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def add_member(request):
	if(check_user(request) == True):
		if request.method == "GET":
			message = ""
			try:
				message = request.session["message"]
				del request.session['message']
			except:
				pass
			return render(request,"add_member.html",{'message':message})
		elif request.method == "POST":
			MyForm = Member(request.POST)
			if MyForm.is_valid():
				username = MyForm.cleaned_data['username']
				user = CCTM.objects.filter(username=username)
				if not user:
					try:
						user = Student.objects.get(username=username)
						if user:
							MyNewForm = CCTM()
							MyNewForm.username = username
							MyNewForm.password = user.password
							MyNewForm.Type = "cctm"
							MyNewForm.save()
							request.session['message'] = "Member "+username+" added successfully"
							message = "You are added as member to Coding Club\nYou can create and manage coding contests\nThanks regards\nCoding Club"
							subject = "Regarding Coding Club"
							mail_id = user.mail
							send_email(mail_id,subject,message)
							return redirect('/manage_accounts')
					except:
						request.session['message'] = "User "+username+" should be a student"
						return redirect('/add_member')
				else:
					request.session['message'] = "Member "+username+" Already Existed"
					return redirect('/add_member')
			return redirect('/manage_accounts')
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def remove_member(request,username):
	if(check_user(request) == True):
		member = CCTM.objects.get(username=username)
		member.delete()
		message = "Sorry, You are removed from Coding Club\nCoding Club"
		user = Student.objects.get(username=username)
		subject = "Regarding Coding Club"
		mail_id = user.mail
		send_email(mail_id,subject,message)
		request.session['message'] = "Member "+username+" Removed Successfully"
		return redirect("/manage_accounts")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def add_online_contest(request):
	if(check_user(request) == True):
		if request.method == "GET":
			return render(request,"add_online_contest.html")
		elif request.method == "POST":
			Form = Online_Contest_Form(request.POST)
			Form.save()
			request.session['message']="online contest added successfully"
			return redirect("/online_contests")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def edit_online_contest(request,id):
	if(check_user(request) == True):
		online_contest = Online_Contest.objects.get(id=id)
		return render(request,"edit_online_contest.html",{'online_contest':online_contest})
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def update_online_contest(request,id):
	if(check_user(request) == True):
		online_contest = Online_Contest.objects.get(id=id)
		Form = Online_Contest_Form(request.POST,instance=online_contest)
		Form.save()
		request.session['message']="online contest updated successfully"
		return redirect("/online_contests")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def delete_online_contest(request,id):
	if(check_user(request) == True):
		contest = Online_Contest.objects.get(id=id)
		contest.delete()
		request.session['message']="online contest deleted successfully"
		return redirect("/online_contests")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def manage_challenges(request):
	if(check_user(request) == True):
		message = ""
		try:
			message = request.session["message"]
			del request.session["message"]
		except:
			pass
		challenges = Create_Challenge.objects.all()
		return render(request,"manage_challenges.html",{'challenges':challenges,'message':message})
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def create_challenge(request):
	if(check_user(request) == True):
		if request.method == "GET":
			return render(request,"create_challenge.html")
		elif request.method == "POST":
			MyForm = Create_Challenge_Form(request.POST)
			if MyForm.is_valid():
				challenge = Create_Challenge.objects.filter(challenge_name=MyForm.cleaned_data['challenge_name'])
				if(not challenge):
					Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Challenges/"+MyForm.cleaned_data['challenge_name']
					os.mkdir(Path)
					NewForm = Create_Challenge()
					NewForm.challenge_name = MyForm.cleaned_data["challenge_name"]
					NewForm.difficulty_level = MyForm.cleaned_data["difficulty_level"]
					NewForm.created_by = request.session["username"]
					NewForm.save()
					f1 = open(Path+"/problem_statement.txt","w")
					f1.write(MyForm.cleaned_data['problem_statement'])
					f1.close()
					f1 = open(Path+"/input_format.txt","w")
					f1.write(MyForm.cleaned_data['input_format'])
					f1.close()
					f1 = open(Path+"/constraints.txt","w")
					f1.write(MyForm.cleaned_data['constraints'])
					f1.close()
					f1 = open(Path+"/output_format.txt","w")
					f1.write(MyForm.cleaned_data['output_format'])
					f1.close()
					f1 = open(Path+"/approach.txt","w")
					f1.write("")
					f1.close()
					f1 = open(Path+"/editorial.txt","w")
					f1.write("")
					f1.close()
					languages_list = ["C","CPP","JAVA","PYTHON2","PYTHON3"]
					for i in languages_list:
						Language = Languages()
						Language.language = i
						Language.challenge_name = MyForm.cleaned_data['challenge_name']
						Language.challenge_id = NewForm
						Language.save()
					request.session['message']="challenge "+str(MyForm.cleaned_data["challenge_name"])+" created successfully"	
				else:
					request.session['message']="challenge "+str(MyForm.cleaned_data["challenge_name"])+" Already Existed"	
				return redirect("/manage_challenges")
			return redirect("/create_challenge")	
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def edit_challenge(request,challenge_name):
	if(check_user(request) == True):
		if request.method == "GET":
			challenge = Create_Challenge.objects.get(challenge_name=challenge_name)
			Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Challenges/"+challenge_name+"/"
			f1 = open(Path+"problem_statement.txt","r")
			problem_statement = f1.read()
			f1.close()
			f1 = open(Path+"input_format.txt","r")
			input_format = f1.read()
			f1.close()
			f1 = open(Path+"output_format.txt","r")
			output_format = f1.read()
			f1.close()
			f1 = open(Path+"constraints.txt","r")
			constraints = f1.read()
			f1.close()
			f1 = open(Path+"approach.txt","r")
			approach = f1.read()
			f1.close()
			f1 = open(Path+"editorial.txt","r")
			code = f1.read()
			f1.close()
			testcases = Testcase.objects.filter(challenge_name=challenge_name)
			for testcase in testcases:
				f1 = open(Path+"input"+str(testcase.id)+".txt","r")
				input = f1.read()
				f1.close()
				testcase.input = input
				f1 = open(Path+"expected_output"+str(testcase.id)+".txt","r")
				output = f1.read()
				f1.close()
				testcase.output = output
				testcase.explanation = ""
				if(testcase.sample == "yes"):
					f1 = open(Path+"explanation"+str(testcase.id)+".txt","r")
					explanation = f1.read()
					f1.close()
					testcase.explanation = explanation
			languages = Languages.objects.filter(challenge_name=challenge_name)
			length = len(testcases)
			return render(request,"edit_challenge.html",{'challenge':challenge,'problem_statement':problem_statement,'input_format':input_format,'output_format':output_format,'constraints':constraints,'approach':approach,'code':code,'testcases':testcases,'length':length,'languages':languages})
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def update_challenge(request,challenge_name):
	if(check_user(request) == True):
		MyForm = Create_Challenge_Form(request.POST)
		if MyForm.is_valid():
			Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Challenges/"+MyForm.cleaned_data['challenge_name']
			NewForm = Create_Challenge.objects.get(challenge_name=challenge_name)
			NewForm.challenge_name = MyForm.cleaned_data["challenge_name"]
			NewForm.difficulty_level = MyForm.cleaned_data["difficulty_level"]
			NewForm.created_by = request.session["username"]
			NewForm.save()
			f1 = open(Path+"/problem_statement.txt","w")
			f1.write(MyForm.cleaned_data['problem_statement'])
			f1.close()
			f1 = open(Path+"/input_format.txt","w")
			f1.write(MyForm.cleaned_data['input_format'])
			f1.close()
			f1 = open(Path+"/constraints.txt","w")
			f1.write(MyForm.cleaned_data['constraints'])
			f1.close()
			f1 = open(Path+"/output_format.txt","w")
			f1.write(MyForm.cleaned_data['output_format'])
			f1.close()
			f1 = open(Path+"/approach.txt","w")
			f1.write("")
			f1.close()
			f1 = open(Path+"/editorial.txt","w")
			f1.write("")
			f1.close()
			request.session['message']="challenge details of "+challenge_name+" updated successfully"
			return redirect("/manage_challenges")	
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")

def update_languages(request,challenge_name):
	languages_list = list(request.POST.getlist('languages'))
	languages = Languages.objects.filter(challenge_name=challenge_name)
	for Language in languages:
		if(Language.language not in languages_list):
			Language.delete()
		elif(Language.language in languages_list):
			languages_list.remove(Language.language)
	challenge_object = Create_Challenge.objects.get(challenge_name=challenge_name)
	for Language in languages_list:
		L = Languages()
		L.challenge_name = challenge_name
		L.challenge_id=challenge_object
		L.language = Language
		L.save()
	request.session['message']="Allowed languages of "+challenge_name+" are updated"
	return redirect("/manage_challenges")

def update_editorial(request,challenge_name):
	if(check_user(request) == True):
		Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Challenges/"+challenge_name+"/"
		Form = Editorial(request.POST)
		if Form.is_valid():
			f1 = open(Path+"approach.txt","w")
			f1.write(Form.cleaned_data["approach"])
			f1.close()
			f1 = open(Path+"editorial.txt","w")
			f1.write(Form.cleaned_data["code"])
			f1.close()
			request.session['message']="editorial of "+challenge_name+" updated successfully"
			return redirect("/manage_challenges")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def add_testcase(request,challenge_name):
	if(check_user(request) == True):
		Form = TestcaseForm(request.POST)
		Form1 = TestcaseForm1(request.POST)
		s1 = Form.is_valid()
		s2 = Form1.is_valid()
		if s1 or s2:
			if s1 == True:
				Form = Form
			else:
				Form = Form1
			Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Challenges/"+challenge_name+"/"
			testcase = Testcase()
			if s1 == True:
				testcase.sample = Form.cleaned_data['sample']
			else:
				testcase.sample = "no"
			testcase.score = int(Form.cleaned_data['score'])
			testcase.challenge_name = challenge_name
			challenge_object = Create_Challenge.objects.get(challenge_name=challenge_name)
			testcase.challenge_id=challenge_object
			testcase.save()
			testcases = Testcase.objects.filter(challenge_name=challenge_name)
			testcase_id = 0
			for t in testcases:
				if testcase_id < t.id:
					testcase_id = t.id
			testcase_id = str(testcase_id)
			f1 = open(Path+"input"+testcase_id+".txt","w")
			f1.write(Form.cleaned_data["input"])
			f1.close()
			f1 = open(Path+"expected_output"+testcase_id+".txt","w")
			f1.write(Form.cleaned_data["output"])
			f1.close()
			if(s1 == True):
				f1 = open(Path+"explanation"+testcase_id+".txt","w")
				f1.write(Form.cleaned_data["explanation"])
				f1.close()
			request.session['message']="testcase added successfully to "+challenge_name
			return redirect("/manage_challenges")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def update_testcase(request,challenge_name,id):
	if(check_user(request) == True):
		Form = TestcaseForm(request.POST)
		Form1 = TestcaseForm1(request.POST)
		s1 = Form.is_valid()
		s2 = Form1.is_valid()
		if s1 or s2:
			if s1 == True:
				Form = Form
			else:
				Form = Form1
			Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Challenges/"+challenge_name+"/"
			testcase = Testcase.objects.get(id=id)
			if s1 == True:
				testcase.sample = Form.cleaned_data['sample']
			else:
				testcase.sample = "no"
			testcase.score = int(Form.cleaned_data['score'])
			testcase.challenge_name = challenge_name
			testcase.save()
			f1 = open(Path+"input"+str(id)+".txt","w")
			f1.write(Form.cleaned_data["input"])
			f1.close()
			f1 = open(Path+"expected_output"+str(id)+".txt","w")
			f1.write(Form.cleaned_data["output"])
			f1.close()
			if(s1 == True):
				f1 = open(Path+"explanation"+str(id)+".txt","w")
				f1.write(Form.cleaned_data["explanation"])
				f1.close()
			request.session['message']="testcase "+str(id)+" of "+challenge_name+" updated successfully"
			return redirect("/manage_challenges")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")
def delete_testcase(request,challenge_name,id):
	if(check_user(request) == True):
		testcase = Testcase.objects.get(id=id)
		testcase.delete()
		Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Challenges/"+challenge_name+"/"
		os.remove(Path+"input"+str(id)+".txt")
		os.remove(Path+"expected_output"+str(id)+".txt")
		if os.path.exists(Path+"explanation"+str(id)+".txt"):
			os.remove(Path+"explanation"+str(id)+".txt")
			request.session['message']="testcase "+str(id)+"of"+challenge_name+" deleted successfully"
		return redirect("/manage_challenges")
	elif(check_user(request) == "student"):
		return redirect("/student_home")
	elif(check_user(request) == False):
		return redirect("/index")

def delete_campus_contest(request,id):
	Path = "/home/rgukt-rkv/CCMS/ccms/Admin/Contests/"
	contest = Create_Campus_Contest.objects.get(id=id)
	request.session['message']="Campus contest "+(contest.contest_name)+" deleted successfully"
	shutil.rmtree(Path+(contest.contest_name))
	contest.delete()
	return redirect("/manage_compete")

def delete_challenge(request,id):
	Path = "/home/rgukt-rkv/CCMS/ccms/Admin/Challenges/"
	challenge = Create_Challenge.objects.get(id=id)
	request.session['message']="Challenge "+(challenge.challenge_name)+" deleted successfully"
	shutil.rmtree(Path+(challenge.challenge_name))
	challenge.delete()
	return redirect("/manage_challenges")
def clear_message_session(request):
	try:
		del request.session["cctm_message"]
		del request.session["student_message"]
		del request.session['user']
	except:
		pass

