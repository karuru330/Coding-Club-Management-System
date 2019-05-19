from django import forms
from ccms.models import Student
from ccms.models import CCTM, Create_Campus_Contest, Online_Contest, Create_Challenge
class StudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = "__all__"
class StudentLogin(forms.Form):
	username = forms.CharField(max_length=7)
	password = forms.CharField(max_length=20)

class CCTMForm(forms.ModelForm):
	class Meta:
		model = CCTM
		fields = "__all__"
class CCTMLogin(forms.Form):
	username = forms.CharField(max_length=7)
	password = forms.CharField(max_length=20)

class Create_Campus_ContestForm(forms.ModelForm):
	class Meta:
		model = Create_Campus_Contest
		fields = "__all__"
class Create_Campus_Contest_Form(forms.Form):
	contest_name = forms.CharField(max_length=50)
	organizer = forms.CharField(max_length=50)
	contest_type = forms.CharField(max_length=20)
	start_date = forms.DateField()
	start_time = forms.CharField(max_length=10)
	end_date = forms.DateField()
	end_time = forms.CharField(max_length=10)
	description = forms.CharField(max_length=5000)
	prizes = forms.CharField(max_length=5000)
	rules = forms.CharField(max_length=5000)
	scoring = forms.CharField(max_length=5000)
class Editorial(forms.Form):
	approach = forms.CharField(max_length=5000)
	code = forms.CharField(max_length=5000)

class Online_Contest_Form(forms.ModelForm):
	class Meta:
		model = Online_Contest
		fields = "__all__"
class Create_Challenge_Form(forms.Form):
	challenge_name = forms.CharField(max_length=50)
	difficulty_level = forms.CharField(max_length=20)
	problem_statement = forms.CharField(max_length=2000)	
	input_format = forms.CharField(max_length=2000)
	constraints = forms.CharField(max_length=2000)
	output_format = forms.CharField(max_length=2000)
class Member(forms.Form):
	username = forms.CharField(max_length=7)
class TestcaseForm(forms.Form):
	sample = forms.CharField(max_length=5)
	score = forms.CharField(max_length=10)
	input = forms.CharField(max_length=5000)
	output = forms.CharField(max_length=5000)
	explanation = forms.CharField(max_length=5000)
class TestcaseForm1(forms.Form):
	score = forms.CharField(max_length=10)
	input = forms.CharField(max_length=5000)
	output = forms.CharField(max_length=5000)
class Contest_Challenges_Form(forms.Form):
	challenge_name = forms.CharField(max_length=50)
	score = forms.CharField(max_length=50)
class Participant_Form(forms.Form):
	username = forms.CharField(max_length=7)
class Notification_Form(forms.Form):
	message = forms.CharField(max_length=5000)
class Code(forms.Form):
	language = forms.CharField(max_length=10)
	code = forms.CharField(max_length=5000)
