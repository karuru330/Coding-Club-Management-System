from django.db import models
class Student(models.Model):
	username = models.CharField(max_length=7)
	password = models.CharField(max_length=20)
	Type = models.CharField(max_length=10)
	mail = models.EmailField()
	class Meta:
		db_table = "student"
class CCTM(models.Model):
	username = models.CharField(max_length=7)
	password = models.CharField(max_length=20)
	Type = models.CharField(max_length=10)
	class Meta:
		db_table = "cctm"

class Create_Campus_Contest(models.Model):
	contest_name = models.CharField(max_length=50)
	organizer = models.CharField(max_length=50)
	contest_type = models.CharField(max_length=20)
	start_date = models.DateField()
	start_time = models.CharField(max_length=10)
	end_date = models.DateField()
	end_time = models.CharField(max_length=10)
	description = models.CharField(max_length=5000)
	prizes = models.CharField(max_length=5000)
	rules = models.CharField(max_length=5000)
	scoring = models.CharField(max_length=5000)
	class Meta:
		db_table = "campus_contests"
class Online_Contest(models.Model):
	contest_name = models.CharField(max_length=50)
	contest_link = models.CharField(max_length=50)
	contest_type = models.CharField(max_length=20)
	start_date = models.DateField()
	start_time = models.CharField(max_length=10)
	end_date = models.DateField()
	end_time = models.CharField(max_length=10)
	class Meta:
		db_table = "online_contests"
class Create_Challenge(models.Model):
	challenge_name = models.CharField(max_length=50)
	difficulty_level = models.CharField(max_length=20)
	created_by = models.CharField(max_length=7)
	class Meta:
		db_table = "challenges"
class Testcase(models.Model):
	sample = models.CharField(max_length=5)
	score = models.DecimalField(max_digits=4,decimal_places=0)
	challenge_name = models.CharField(max_length=50)
	challenge_id = models.ForeignKey(Create_Challenge,on_delete=models.CASCADE)
	class Meta:
		db_table = "testcases"
class Contest_Challenges(models.Model):
	challenge_name =  models.CharField(max_length=50)
	score = models.DecimalField(max_digits=4,decimal_places=0)
	challenge_id = models.ForeignKey(Create_Challenge,on_delete=models.CASCADE)
	contest_name = models.CharField(max_length=50)
	contest_id = models.ForeignKey(Create_Campus_Contest,on_delete=models.CASCADE)
	class Meta:
		db_table = "contest_challenges"
class Participant(models.Model):
	username = models.CharField(max_length=7)
	contest_name = models.CharField(max_length=50)
	contest_id = models.ForeignKey(Create_Campus_Contest,on_delete=models.CASCADE)
	class Meta:
		db_table = "participants"
class Notification(models.Model):
	username = models.CharField(max_length=7)
	message = models.CharField(max_length=5000)
	contest_name = models.CharField(max_length=50)
	date = models.DateField()
	time = models.CharField(max_length=10)
	class Meta:
		db_table = "notifications"
class Submissions(models.Model):
	challenge_name = models.CharField(max_length=50)
	contest_name = models.CharField(max_length=50)
	score = models.DecimalField(max_digits=4,decimal_places=0)
	time = models.CharField(max_length=10)
	language = models.CharField(max_length=10)
	status = models.CharField(max_length=20)
	username = models.CharField(max_length=7)
	date = models.DateField()
	class Meta:
		db_table = "submissions"
class Challenges_Leaderboard(models.Model):
	username = models.CharField(max_length=7)
	contest_name = models.CharField(max_length=50)
	challenge_name = models.CharField(max_length=50)
	time = models.CharField(max_length=10)
	score = models.DecimalField(max_digits=4,decimal_places=0)
	class Meta:
		db_table = "challenges_leaderboard"
class Contest_Leaderboard(models.Model):
	username = models.CharField(max_length=7)
	contest_name = models.CharField(max_length=50)
	time = models.CharField(max_length=10)
	score = models.DecimalField(max_digits=4,decimal_places=0)
	class Meta:
		db_table = "contest_leaderboard"
class Languages(models.Model):
	challenge_id = models.ForeignKey(Create_Challenge,on_delete=models.CASCADE)
	challenge_name = models.CharField(max_length=50)
	language = models.CharField(max_length=20)
	class Meta:
		db_table = "languages"
class Leaderboard(models.Model):
	username = models.CharField(max_length=7)
	rating = models.DecimalField(max_digits=4,decimal_places=0)
	class Meta:
		db_table = "leaderboard"
