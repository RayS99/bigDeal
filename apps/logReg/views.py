from django.shortcuts import render, HttpResponse, redirect
from .models import User, Post
from django.contrib import auth
import bcrypt
import re
from django.contrib.messages import error

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
UltKey = 'userId'
# Views file is where functions are made for routes to execute.
def index(request):
    return render(request, 'logReg/index.html')

def enterSite(request):
	print('-----enterSite-----')
	if request.method == 'POST':
		errors = []
		userGate = User.objects.filter(email=request.POST['email'])
		if not userGate:
			errors.append('Incorrect Data')
		else:
			if not bcrypt.checkpw(request.POST['password'].encode(), userGate[0].password.encode()):
				errors.append('Incorrect Data')
		if errors:
			for e in errors:
				error(request, e)
			return redirect('/')
		request.session[UltKey] = userGate[0].id
		return redirect('/wall')
	return redirect('/')

def registration(request):
	print('-----registration-----'*5)
	if request.method == 'POST':
		print(request.POST)
		#List below holds list of 
		errors = []
		if(len(request.POST['user_name'])<1):
			errors.append("User required!")
		if(len(request.POST['email']) < 1):
			errors.append('Email required!')
		if(len(request.POST['password']) < 1):
			errors.append("You need a password fool!")
		if(request.POST['password'] != request.POST['cpassword']):
			errors.append('Must match password fields')
		if not re.match(EMAIL_REGEX, request.POST['email']):
			errors.append("This aint no email!")
		if not errors:
			hashed = bcrypt.hashpw(request.POST['cpassword'].encode(), bcrypt.gensalt())
			lateUser = User.objects.create(user_name = request.POST['user_name'], email = request.POST['email'], password = hashed)
			request.session[UltKey] = lateUser.id
			#request.POST same as request.form in Flask
		else:
			for err in errors:
				error(request, err)
			print(errors)
			return redirect('/')

		return redirect('/wall')

# def display(request, user_id):
# 	user = User.objects.get(id=user_id)
# 	context = {
# 	 "user" : user
# 	}
# 	return redirect("/wall")

def wall(request):
	print("-----wall-----"*5)
	try:
		user_id = request.session[UltKey]
	except:
		return redirect('/')
	# order=['-date_posted']
	context = {
		'user' : User.objects.get(id=user_id),
		'postits' : Post.objects.all()
	}
	return render(request, 'logReg/wall.html', context)



def createPost(request):
	#make sure post is not empty.
	print('-----createPost-----'*5)
	errors = []
	if len(request.POST['post']) < 1:
		errors.append("No empty shares")
	if len(request.POST['post']) > 255:
		errors.append("You talk'n too much bruv!")
	if len(errors)==0:
		myUser = User.objects.get(id=request.session[UltKey])
		myPost=Post.objects.create(content = request.POST['post'], author = myUser)
		# userLink = session.request['author.id']
	else:
		for err in errors:
			error(request, err)
		print(errors)
		return redirect('/wall')
	return redirect('/wall')

def deletePost(request,post_id):
	print('-----deletePost-----'*5)
	print(post_id)
	myPost = Post.objects.get(id=post_id)
	inUser = User.objects.get(id=request.session[UltKey])
	postCreator=myPost.author_id
	creator=inUser.id
	if postCreator==creator:
		myPost.delete()
	return redirect('/wall')


def editPost(request, post_id):
	print('-----editPost-----'*5)
	context={
		"change" : Post.objects.get(id=post_id),
		'user' : User.objects.get(id=request.session[UltKey]),
	}
	myPost = Post.objects.get(id=post_id)
	inUser = User.objects.get(id=request.session[UltKey])
	postCreator=myPost.author_id
	creator=inUser.id
	if request.method == 'GET' and postCreator==creator:
		return render(request,"logReg/edit.html", context)
	return redirect('/wall')


def updatePost(request,post_id):
	print('-----updatePost-----'*5)
	if request.method == 'POST':
		myPost=post_id
		print(myPost)
		myPost = Post.objects.get(id=post_id)
		inUser = User.objects.get(id=request.session[UltKey])
		# aPost=Post.objects.get(author_id=inUser)
		postCreator=myPost.author_id
		creator=inUser.id
		errors = []
		if len(request.POST['post']) < 1:
			errors.append("No empty shares")
		if len(request.POST['post']) > 255:
			errors.append("You talk'n too much bruv!")
		if (len(errors)==0) and (postCreator==creator):
			IDone = Post.objects.get(id=post_id)
			IDone.content=request.POST['post']
			IDone.save()
			return redirect('/wall')
		else:
			context={
				"change" : Post.objects.get(id=post_id),
				'user' : User.objects.get(id=request.session[UltKey]),
			}
			for err in errors:
				error(request, err)
			print(errors)
			return render(request, 'logReg/edit.html', context)
	return redirect('/wall')


def exitSite(request):
	print('-----exitSite-----'*5)
	return redirect('/')