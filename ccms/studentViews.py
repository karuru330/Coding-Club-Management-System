from django.shortcuts import render,redirect
from django.http import HttpResponse
from ccms.forms import StudentLogin,Code
from ccms.models import Student, Create_Campus_Contest, Online_Contest,Participant,CCTM,Contest_Challenges,Create_Challenge,Testcase,Submissions,Challenges_Leaderboard,Contest_Leaderboard,Notification,Languages
import datetime
from datetime import datetime
import time
import pytz
import subprocess
import os
from datetime import date
import datetime as dt
def student_login(request):
	username = ""
	password = ""
	clear_message_session(request)
	if(request.method == "POST"):
		MyLoginForm = StudentLogin(request.POST)
		if(MyLoginForm.is_valid()):
			username = MyLoginForm.cleaned_data['username']
			password = MyLoginForm.cleaned_data['password']
			dbuser = Student.objects.filter(username=username,password=password)
			if not dbuser:
				request.session['student_message']="Incorrect username or password"
				request.session['user'] = 'student'
				return redirect("/index")
			request.session['username'] = username
			request.session['type'] = 'student'
			request.session['student_message'] = ""
			request.session['user'] = 'cctm'
			return redirect('/student_home')
		else:
			request.session['student_message']=""
			request.session['user'] = 'student'
			return redirect("/index")
def student_home(request):
	clear_message_session(request)
	try:
		if(request.session['username']!=None and request.session['type']=="student"):
			request.session['student_message'] = ""
			request.session['user'] = 'student'
			return render(request,"student_home.html")
		elif(request.session['username']!=None and request.session['type']=="cctm"):
			request.session['student_message'] = ""
			request.session['user'] = 'student'
			return redirect("/cctm_home")
		else:
			request.session['student_message']="You are not logged in .."
			request.session['user'] = 'student'
			return redirect("/index")
	except:
		request.session['student_message']="You are not logged in .."
		request.session['user'] = 'student'
		return redirect("/index")

def student_logout(request):
	clear_message_session(request)
	try:
		del request.session['username']
		del request.session['type']
	except:
		pass
	request.session['student_message']="You are successfully logged out .."
	request.session['user'] = 'student'
	return redirect("/index")
def compete(request):
	return redirect("/compete/campus_contests")
def campus_contests(request):
	campus_contests = Create_Campus_Contest.objects.all()
	return render(request,"compete.html",{'campus_contests':campus_contests,'tab_status':'campus'})
def online_contests(request):
	online_contests = Online_Contest.objects.all()
	return render(request,"compete.html",{'online_contests':online_contests,'tab_status':'online'})
def contest_home(request,contest_name):
	campus_contest = Create_Campus_Contest.objects.get(contest_name=contest_name)
	about = []
	Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Contests/"+contest_name+"/"
	f1 = open(Path+"description.txt","r")
	data = f1.readline()
	while data:
		about.append(data)
		data = f1.readline()
	prizes=[]
	f1 = open(Path+"prizes.txt","r")
	data = f1.readline()
	while data:
		prizes.append(data)
		data = f1.readline()
	rules=[]
	f1 = open(Path+"rules.txt","r")
	data = f1.readline()
	while data:
		rules.append(data)
		data = f1.readline()
	scoring=[]
	f1 = open(Path+"scoring.txt","r")
	data = f1.readline()
	while data:
		scoring.append(data)
		data = f1.readline()
	return render(request,"contest_home.html",{'campus_contest':campus_contest,'about':about,'prizes':prizes,'rules':rules,'scoring':scoring})

def notifications(request):
	username = request.session['username']
	notifications = Notification.objects.filter(username=username)
	return render(request,"notifications.html",{'notifications':notifications})
def contest_page(request,contest_name):
	username = request.session['username']
	participant = Participant.objects.filter(contest_name=contest_name,username=username)
	cctm = CCTM.objects.filter(username=username)
	if (not participant) and (not cctm):
		return redirect("/not_allowed_page")
	status,date_time = get_contest_status(contest_name)
	contest_challenges = {}
	if(status == "ended"):
		contest_challenges = Contest_Challenges.objects.filter(contest_name=contest_name)
	elif(status == "progress"):
		contest_challenges = Contest_Challenges.objects.filter(contest_name=contest_name)
	if(cctm):
		contest_challenges = Contest_Challenges.objects.filter(contest_name=contest_name)
	return render(request,"contest_challenges.html",{'contest_challenges':contest_challenges,'date_time':date_time,'status':status,'contest_name':contest_name})
def challenge_info(request,contest_name,challenge_name):
	Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Challenges/"+challenge_name+"/"
	challenge = Create_Challenge.objects.get(challenge_name=challenge_name)
	f1 = open(Path+"problem_statement.txt","r")
	problem_statement = str(f1.read())
	f1.close()
	f1 = open(Path+"input_format.txt","r")
	input_format = (f1.read())
	f1.close()
	f1 = open(Path+"constraints.txt","r")
	constraints = (f1.read())
	f1.close()
	f1 = open(Path+"output_format.txt","r")
	output_format = (f1.read())
	f1.close()
	
	testcases = Testcase.objects.filter(challenge_name=challenge_name,sample="yes")
	i=0
	for testcase in testcases:
		testcase_id = str(testcase.id)
		f1 = open(Path+"input"+testcase_id+".txt","r")
		testcase.input = f1.read()
		f1.close()
		f1 = open(Path+"expected_output"+testcase_id+".txt","r")
		testcase.output = f1.read()
		f1.close()
		f1 = open(Path+"explanation"+testcase_id+".txt","r")
		testcase.explanation = f1.read()
		f1.close()
		testcase.input_header = "Sample Input "+str(i)
		testcase.output_header = "Sample Output "+str(i)
		testcase.explanation_header = "Explanation "+str(i)
		i=i+1
	status,date_time = get_contest_status(contest_name)
	username = request.session['username']
	languages = Languages.objects.filter(challenge_name=challenge_name)
	return render(request,"challenge.html",{'problem_statement':problem_statement,'input_format':input_format,'constraints':constraints,'output_format':output_format,'challenge':challenge,'testcases':testcases,'contest_name':contest_name,'status':status,'date_time':date_time,'tab_status':'problem_statement','challenge_name':challenge_name,'username':username,'languages':languages})

def get_submissions(request,contest_name,challenge_name):
	challenge = Create_Challenge.objects.get(challenge_name=challenge_name)
	username = request.session['username']
	submissions = Submissions.objects.filter(contest_name=contest_name,challenge_name=challenge_name,username=username).order_by('-date','-time')
	i = 1
	for submission in submissions:
		submission.sno = i
		i=i+1
	status,date_time = get_contest_status(contest_name)
	return render(request,"challenge.html",{'submissions':submissions,'tab_status':'submissions','status':status,'date_time':date_time,'challenge_name':challenge_name,'contest_name':contest_name,'challenge':challenge})

def get_challenges_leaderboard(request,contest_name,challenge_name):
	challenge = Create_Challenge.objects.get(challenge_name=challenge_name)
	username = request.session['username']
	leaderboard = Challenges_Leaderboard.objects.filter(contest_name=contest_name,challenge_name=challenge_name).order_by('-score','time')
	i = 1
	for row in leaderboard:
		row.sno = i
		i = i+1
	status,date_time = get_contest_status(contest_name)
	return render(request,"challenge.html",{'leaderboard':leaderboard,'tab_status':'leaderboard','status':status,'date_time':date_time,'challenge_name':challenge_name,'contest_name':contest_name,'challenge':challenge})

def get_editorial(request,contest_name,challenge_name):
	challenge = Create_Challenge.objects.get(challenge_name=challenge_name)
	username = request.session['username']
	status,date_time = get_contest_status(contest_name)
	approach = ""
	solution = ""
	if status == "ended":
		Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Challenges/"+challenge_name+"/"
		fd1 = open(Path+"approach.txt","r")
		approach = fd1.read()
		fd1.close()
		fd2 = open(Path+"editorial.txt","r")
		solution = fd2.read()
		fd2.close()
		if(approach == ""):
			approach = "None"
		if(solution == ""):
			solution = "None"
	return render(request,"challenge.html",{'tab_status':'editorial','status':status,'date_time':date_time,'approach':approach,'solution':solution,'challenge_name':challenge_name,'contest_name':contest_name,'challenge':challenge})

def get_contest_leaderboard(request,contest_name):
	leaderboard = Contest_Leaderboard.objects.filter(contest_name=contest_name).order_by('-score','time')
	i = 1
	for row in leaderboard:
		row.sno = i
		i = i+1
	return render(request,"contest_leaderboard.html",{'leaderboard':leaderboard,'contest_name':contest_name})
def get_contest_status(contest_name):
	contest = Create_Campus_Contest.objects.get(contest_name=contest_name)
	stime = contest.start_time
	sdate = contest.start_date
	sdate = str(sdate)
	sdate = sdate[2:]
	sdate = sdate[6:8]+"/"+sdate[3:5]+"/"+sdate[0:2]
	sdate = sdate.replace("-","/")
	start_date_time = datetime.strptime(sdate+" "+str(stime),'%d/%m/%y %H:%M:%S')
	etime = contest.end_time
	edate = contest.end_date
	edate = str(edate)
	edate = edate[2:]
	edate = edate[6:8]+"/"+edate[3:5]+"/"+edate[0:2]
	edate = edate.replace("-","/")
	current = str(datetime.now())
	end_date_time = datetime.strptime(edate+" "+str(etime),'%d/%m/%y %H:%M:%S')
	cdate = current[2:]
	cdate = cdate[6:8]+"/"+cdate[3:5]+"/"+cdate[0:2]
	tz = pytz.timezone('Asia/Kolkata')
	ctime = str(datetime.now(tz).time())
	ctime = ctime[0:8]
	current_date_time = datetime.strptime(cdate+" "+str(ctime),'%d/%m/%y %H:%M:%S')
	status = ""
	date_time = ""
	if(current_date_time>=end_date_time):
		status = "ended"
		contest_challenges = Contest_Challenges.objects.filter(contest_name=contest_name)
	elif((current_date_time>=start_date_time) and (current_date_time<=end_date_time)):
		status = "progress" 
		date_time = str(contest.end_date)+" "+str(contest.end_time)
		contest_challenges = Contest_Challenges.objects.filter(contest_name=contest_name)
	else:
		status = "not started"
		date_time = str(contest.start_date)+" "+str(contest.start_time)
	return (status,date_time)
def submit(request,contest_name,challenge_name):
	Form = Code(request.POST)
	Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Challenges/"+challenge_name+"/"
	user = request.session["username"]
	if Form.is_valid():
		language = Form.cleaned_data["language"]
		extension = ""
		contest = contest_name.replace(" ","_")
		if(language == "C"):
			extension = ".c"
		elif(language == "CPP"):
			extension = ".cpp"
		elif(language == "JAVA"):
			extension = ".java"
		elif(language == "PYTHON2" or language == "PYTHON3"):
			extension = ".py"
		contest = contest_name.replace(" ","_")
		try:
			f = request.FILES['file']
			
			with open(Path+user+"_"+contest+extension,"wb+") as destination:
				for chunk in f.chunks():
					destination.write(chunk)
		except:
			
			filename = Path+user+"_"+contest+extension
			f1 = open(filename,"w")
			f1.write(Form.cleaned_data["code"])
			f1.close()
		path = Path+user+"_"+contest_name
		testcases = {}
		if(language == "C"):
			command = "gcc -o "+user+"_"+contest+"_"+language+" "+user+"_"+contest+extension
			proc = subprocess.Popen("cd 'ccms/Admin/Challenges/"+challenge_name+"' && "+command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
			err = proc.stderr.read()
			if(err!=""):
				make_submission(0,"Compile Error",user,contest_name,challenge_name,language)
				return render(request,"response.html",{'status':'Compile Error','message':err})
			else:
				testcases = Testcase.objects.filter(challenge_name=challenge_name)
				for testcase in testcases:
					Id = testcase.id
					fd = open(Path+"input"+str(Id)+".txt","r")
					proc = subprocess.Popen("ccms/Admin/Challenges/"+challenge_name+"/"+user+"_"+contest+"_"+language,shell=True,stdin=fd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
					fd.close()
					output = str(proc.stdout.read())
					fd1 = open(Path+user+"_"+contest+"_"+language+"_user_output"+str(Id)+".txt","w")
					fd1.write(output)
					fd1.close()
		elif(language == "CPP"):
			command = "g++ -o "+user+"_"+contest+"_"+language+" "+user+"_"+contest+extension
			proc = subprocess.Popen("cd 'ccms/Admin/Challenges/"+challenge_name+"' && "+command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
			err = proc.stderr.read()
			if(err!=""):
				make_submission(0,"Compile Error",user,contest_name,challenge_name,language)
				return render(request,"response.html",{'status':'Compile Error','message':err})
			else:
				testcases = Testcase.objects.filter(challenge_name=challenge_name)
				for testcase in testcases:
					Id = testcase.id
					fd = open(Path+"input"+str(Id)+".txt","r")
					proc = subprocess.Popen("ccms/Admin/Challenges/"+challenge_name+"/"+user+"_"+contest+"_"+language,shell=True,stdin=fd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
					fd.close()
					output = str(proc.stdout.read())
					fd1 = open(Path+user+"_"+contest+"_"+language+"_user_output"+str(Id)+".txt","w")
					fd1.write(output)
					fd1.close()
		elif(language == "PYTHON2"):
			testcases = Testcase.objects.filter(challenge_name=challenge_name)
			err = ""
			proc = subprocess.Popen("cd 'ccms/Admin/Challenges/"+challenge_name+"'",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
			for testcase in testcases:
				Id = testcase.id
				command = "cd 'ccms/Admin/Challenges/"+challenge_name+"' && python2 "+user+"_"+contest+extension+" < "+"input"+str(Id)+".txt"
				proc = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
				output = str(proc.stdout.read())
				err = proc.stderr.read()
				if(err !=""):
					break
				fd1 = open(Path+user+"_"+contest+"_"+language+"_user_output"+str(Id)+".txt","w")
				fd1.write(output)
				fd1.close()
			if(err != ""):
				make_submission(0,"Error",user,contest_name,challenge_name,language)
				return render(request,"response.html",{'status':'Error','message':err})
		elif(language == "PYTHON3"):
			testcases = Testcase.objects.filter(challenge_name=challenge_name)
			err = ""
			proc = subprocess.Popen("cd 'ccms/Admin/Challenges/"+challenge_name+"'",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
			for testcase in testcases:
				Id = testcase.id
				command = "cd 'ccms/Admin/Challenges/"+challenge_name+"' && python3 "+user+"_"+contest+extension+" < "+"input"+str(Id)+".txt"
				proc = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
				output = str(proc.stdout.read())
				err = proc.stderr.read()
				if(err !=""):
					break
				fd1 = open(Path+user+"_"+contest+"_"+language+"_user_output"+str(Id)+".txt","w")
				fd1.write(output)
				fd1.close()
			if(err != ""):
				make_submission(0,"Error",user,contest_name,challenge_name,language)
				return render(request,"response.html",{'status':'Error','message':err})
		elif(language == "JAVA"):
			command = "javac "+user+"_"+contest+extension
			proc = subprocess.Popen("cd 'ccms/Admin/Challenges/"+challenge_name+"' && "+command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
			err = proc.stderr.read()
			if(err!=""):
				make_submission(0,"Compile Error",user,contest_name,challenge_name,language)
				return render(request,"response.html",{'status':'Compile Error','message':err})
			else:
				testcases = Testcase.objects.filter(challenge_name=challenge_name)
				for testcase in testcases:
					Id = testcase.id
					command = "java "+user+"_"+contest
					fd = open(Path+"input"+str(Id)+".txt","r")
					proc = subprocess.Popen("cd ccms/Admin/Challenges/"+challenge_name+" && "+command,shell=True,stdin=fd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
					fd.close()
					output = str(proc.stdout.read())
					fd1 = open(Path+user+"_"+contest+"_"+language+"_user_output"+str(Id)+".txt","w")
					fd1.write(output)
					fd1.close()
		
		status = "Correct Answer"
		score = 0
		count = 0
		for testcase in testcases:
			Id = testcase.id
			fd1 = open(Path+"expected_output"+str(Id)+".txt","r")
			expected_output = fd1.read()
			fd1.close()
			fd2 = open(Path+user+"_"+contest+"_"+language+"_user_output"+str(Id)+".txt","r")
			user_output = fd2.read()
			fd2.close()
			if(expected_output == user_output or expected_output == user_output[0:-1]):
				testcase.status = "Correct Answer"
				score = score+testcase.score
			else:
				testcase.status = "Wrong Answer"
				status = "Wrong Answer"
			testcase.header = count
			testcase.user_output = user_output
			testcase.expected_output = expected_output
			count = count+1
		make_submission(score,status,user,contest_name,challenge_name,language)
		Type = request.session['type']
		make_challenge_leaderboard(user,contest_name,challenge_name,score)
		make_contest_leaderboard(user,contest_name)
		return render(request,"response.html",{'status':status,'message':testcases,'score':score})
	return HttpResponse(Form)

def run(request,contest_name,challenge_name):
	Form = Code(request.POST)
	Path =  "/home/rgukt-rkv/CCMS/ccms/Admin/Challenges/"+challenge_name+"/"
	user = request.session["username"]
	if Form.is_valid():
		language = Form.cleaned_data["language"]
		extension = ""
		contest = contest_name.replace(" ","_")
		if(language == "C"):
			extension = ".c"
		elif(language == "CPP"):
			extension = ".cpp"
		elif(language == "JAVA"):
			extension = ".java"
		elif(language == "PYTHON2" or language == "PYTHON3"):
			extension = ".py"
		contest = contest_name.replace(" ","_")
		try:
			f = request.FILES['file']
			
			with open(Path+user+"_"+contest+extension,"wb+") as destination:
				for chunk in f.chunks():
					destination.write(chunk)
		except:
			
			filename = Path+user+"_"+contest+extension
			f1 = open(filename,"w")
			f1.write(Form.cleaned_data["code"])
			f1.close()
		path = Path+user+"_"+contest_name
		testcases = {}
		if(language == "C"):
			command = "gcc -o "+user+"_"+contest+"_"+language+" "+user+"_"+contest+extension
			proc = subprocess.Popen("cd 'ccms/Admin/Challenges/"+challenge_name+"' && "+command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
			err = proc.stderr.read()
			if(err!=""):
				make_submission(0,"Compile Error",user,contest_name,challenge_name,language)
				return render(request,"result.html",{'status':'Compile Error','message':err})
			else:
				testcases = Testcase.objects.filter(challenge_name=challenge_name,sample="yes")
				for testcase in testcases:
					Id = testcase.id
					fd = open(Path+"input"+str(Id)+".txt","r")
					proc = subprocess.Popen("ccms/Admin/Challenges/"+challenge_name+"/"+user+"_"+contest+"_"+language,shell=True,stdin=fd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
					output = str(proc.stdout.read())
					fd.close()
					fd = open(Path+"input"+str(Id)+".txt","r")
					testcase.input = fd.read()
					fd.close()
					fd1 = open(Path+user+"_"+contest+"_"+language+"_user_output"+str(Id)+".txt","w")
					fd1.write(output)
					fd1.close()
		elif(language == "CPP"):
			command = "g++ -o "+user+"_"+contest+"_"+language+" "+user+"_"+contest+extension
			proc = subprocess.Popen("cd 'ccms/Admin/Challenges/"+challenge_name+"' && "+command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
			err = proc.stderr.read()
			if(err!=""):
				make_submission(0,"Compile Error",user,contest_name,challenge_name,language)
				return render(request,"result.html",{'status':'Compile Error','message':err})
			else:
				testcases = Testcase.objects.filter(challenge_name=challenge_name,sample="yes")
				for testcase in testcases:
					Id = testcase.id
					fd = open(Path+"input"+str(Id)+".txt","r")
					proc = subprocess.Popen("ccms/Admin/Challenges/"+challenge_name+"/"+user+"_"+contest+"_"+language,shell=True,stdin=fd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
					output = str(proc.stdout.read())
					fd.close()
					fd = open(Path+"input"+str(Id)+".txt","r")
					testcase.input = fd.read()
					fd.close()
					fd1 = open(Path+user+"_"+contest+"_"+language+"_user_output"+str(Id)+".txt","w")
					fd1.write(output)
					fd1.close()
		elif(language == "PYTHON2"):
			testcases = Testcase.objects.filter(challenge_name=challenge_name,sample="yes")
			err = ""
			proc = subprocess.Popen("cd 'ccms/Admin/Challenges/"+challenge_name+"'",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
			for testcase in testcases:
				Id = testcase.id
				command = "cd 'ccms/Admin/Challenges/"+challenge_name+"' && python2 "+user+"_"+contest+extension+" < "+"input"+str(Id)+".txt"
				proc = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
				output = str(proc.stdout.read())
				err = proc.stderr.read()
				if(err !=""):
					break
				fd = open(Path+"input"+str(Id)+".txt","r")
				testcase.input = fd.read()
				fd.close()
				fd1 = open(Path+user+"_"+contest+"_"+language+"_user_output"+str(Id)+".txt","w")
				fd1.write(output)
				fd1.close()
			if(err != ""):
				make_submission(0,"Error",user,contest_name,challenge_name,language)
				return render(request,"result.html",{'status':'Error','message':err})
		elif(language == "PYTHON3"):
			testcases = Testcase.objects.filter(challenge_name=challenge_name,sample="yes")
			err = ""
			proc = subprocess.Popen("cd 'ccms/Admin/Challenges/"+challenge_name+"'",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
			for testcase in testcases:
				Id = testcase.id
				command = "cd 'ccms/Admin/Challenges/"+challenge_name+"' && python3 "+user+"_"+contest+extension+" < "+"input"+str(Id)+".txt"
				proc = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
				output = str(proc.stdout.read())
				err = proc.stderr.read()
				if(err !=""):
					break
				fd = open(Path+"input"+str(Id)+".txt","r")
				testcase.input = fd.read()
				fd.close()
				fd1 = open(Path+user+"_"+contest+"_"+language+"_user_output"+str(Id)+".txt","w")
				fd1.write(output)
				fd1.close()
			if(err != ""):
				make_submission(0,"Error",user,contest_name,challenge_name,language)
				return render(request,"result.html",{'status':'Error','message':err})
		elif(language == "JAVA"):
			command = "javac "+user+"_"+contest+extension
			proc = subprocess.Popen("cd 'ccms/Admin/Challenges/"+challenge_name+"' && "+command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
			err = proc.stderr.read()
			if(err!=""):
				make_submission(0,"Compile Error",user,contest_name,challenge_name,language)
				return render(request,"result.html",{'status':'Compile Error','message':err})
			else:
				testcases = Testcase.objects.filter(challenge_name=challenge_name,sample="yes")
				for testcase in testcases:
					Id = testcase.id
					command = "java "+user+"_"+contest
					fd = open(Path+"input"+str(Id)+".txt","r")
					proc = subprocess.Popen("cd ccms/Admin/Challenges/"+challenge_name+" && "+command,shell=True,stdin=fd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
					output = str(proc.stdout.read())
					fd.close()
					fd = open(Path+"input"+str(Id)+".txt","r")
					testcase.input = fd.read()
					fd.close()
					fd1 = open(Path+user+"_"+contest+"_"+language+"_user_output"+str(Id)+".txt","w")
					fd1.write(output)
					fd1.close()
		
		status = "Correct Answer"
		score = 0
		count = 0
		for testcase in testcases:
			Id = testcase.id
			fd1 = open(Path+"expected_output"+str(Id)+".txt","r")
			expected_output = fd1.read()
			fd1.close()
			fd2 = open(Path+user+"_"+contest+"_"+language+"_user_output"+str(Id)+".txt","r")
			user_output = fd2.read()
			fd2.close()
			if(expected_output == user_output or expected_output == user_output[0:-1]):
				testcase.status = "Correct Answer"
				score = score+testcase.score
			else:
				testcase.status = "Wrong Answer"
				status = "Wrong Answer"
			if(user_output == ""):
				user_output = "Your code does not printing anything"
			testcase.header = count
			testcase.user_output = user_output
			testcase.expected_output = expected_output
			count = count+1
		return render(request,"result.html",{'status':status,'message':testcases,'score':score})
	return HttpResponse(Form)
def make_submission(score,status,user,contest_name,challenge_name,language):
	tz = pytz.timezone('Asia/Kolkata')
	time = str(datetime.now(tz).time())
	time = time[0:8]
	Date = str(date.today())
	submission = Submissions()
	submission.contest_name = contest_name
	submission.challenge_name = challenge_name
	submission.score = score
	submission.status = status
	submission.username = user
	submission.language = language
	submission.date = Date
	submission.time = time
	submission.save()
def make_challenge_leaderboard(username,contest_name,challenge_name,score):
	user = CCTM.objects.filter(username=username)
	if(check_time(contest_name) == True and (not user)):
		tz = pytz.timezone('Asia/Kolkata')
		time = str(datetime.now(tz).time())
		time = time[0:8]
		contest = Create_Campus_Contest.objects.get(contest_name=contest_name)
		start_time = contest.start_time
		end_time = contest.end_time
		ch = int(time[0:2])
		cm = int(time[3:5])
		cs = int(time[6:8])
		sh = int(start_time[0:2])
		sm = int(start_time[3:5])
		ss = int(start_time[6:8])
		if(cs>=ss):
			cs = cs-ss
		elif(cs<ss):
			cm = cm-1
			cs = (cs+60)-ss
		if(cm>=sm):
			cm = cm-sm
		elif(cm<sm):
			ch = ch-1
			cm = (cm+60)-sm
		ch = ch-sh
		ch = str(ch)
		cm = str(cm)
		cs = str(cs)
		if(len(ch) == 1):
			ch = "0"+ch
		if(len(cm)==1):
			cm = "0"+cm
		if(len(cs)==1):
			cs = "0"+cs
		result = str(ch)+":"+str(cm)+":"+str(cs)
		try:
			row = Challenges_Leaderboard.objects.get(username=username,contest_name=contest_name,challenge_name=challenge_name)
			old_score = row.score
			if(score>old_score):
				row.score = score
				row.time = result
				row.save()
		except:
			row = Challenges_Leaderboard()
			row.score = score
			row.contest_name = contest_name
			row.challenge_name = challenge_name
			row.username = username
			row.time = result
			row.save()
def make_contest_leaderboard(username,contest_name):
	rows = Challenges_Leaderboard.objects.filter(contest_name=contest_name,username=username)
	h = 0
	m = 0
	s = 0
	score = 0
	count = 0
	for row in rows:
		time = row.time
		h1 = int(time[0:2])
		m1 = int(time[3:5])
		s1 = int(time[6:8])
		s1 = s+s1
		s = int(s1%60)
		m1 = m+(m1+int(s1/60))
		m = int(m1%60)
		h = (h+(h1+int(m1/60)))
		score = score+(row.score)
		count = count+1
	h = str(h)
	m = str(m)
	s = str(s)
	if(len(h) == 1):
		h = "0"+h
	if(len(m) == 1):
		m = "0"+m
	if(len(s) == 1):
		s = "0"+s
	time = h+":"+m+":"+s
	if(count>0):
		try:
			row = Contest_Leaderboard.objects.get(contest_name=contest_name,username=username)
			row.score = score
			row.time = time
			row.save()
		except:
			row = Contest_Leaderboard()
			row.score = score
			row.time = time
			row.contest_name = contest_name
			row.username = username
			row.save()
def check_time(contest_name):
	contest = Create_Campus_Contest.objects.get(contest_name=contest_name)
	stime = contest.start_time
	sdate = contest.start_date
	sdate = str(sdate)
	sdate = sdate[2:]
	sdate = sdate[6:8]+"/"+sdate[3:5]+"/"+sdate[0:2]
	sdate = sdate.replace("-","/")
	start_date_time = datetime.strptime(sdate+" "+str(stime),'%d/%m/%y %H:%M:%S')
	etime = contest.end_time
	edate = contest.end_date
	edate = str(edate)
	edate = edate[2:]
	edate = edate[6:8]+"/"+edate[3:5]+"/"+edate[0:2]
	edate = edate.replace("-","/")
	current = str(datetime.now())
	end_date_time = datetime.strptime(edate+" "+str(etime),'%d/%m/%y %H:%M:%S')
	cdate = current[2:]
	cdate = cdate[6:8]+"/"+cdate[3:5]+"/"+cdate[0:2]
	tz = pytz.timezone('Asia/Kolkata')
	ctime = str(datetime.now(tz).time())
	ctime = ctime[0:8]
	current_date_time = datetime.strptime(cdate+" "+str(ctime),'%d/%m/%y %H:%M:%S')
	if((current_date_time>=start_date_time) and (current_date_time<=end_date_time)):
		return True
	else:
		return False
def not_allowed(request):
	return render(request,"not_allowed_page.html")
	
def clear_message_session(request):
	try:
		del request.session['student_message']
		del request.session['cctm_message']
		del request.session['user']
	except:
		pass
