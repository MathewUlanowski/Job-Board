from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

import bcrypt

# Create your views here.
def default(request):
    return redirect('/login')
def index(request):
    if request.method == "GET":
        return render(request, 'login_handler/index.html')
    elif request.method == "POST":
        user = Users.objects.filter(email=request.POST['loginuser'])
        if len(user) > 0:
            testpass = user.first().password
            if bcrypt.checkpw((request.POST['loginpassword']).encode(), testpass.encode()):
                request.session['user'] = Users.objects.get(email=request.POST['loginuser']).id
                return redirect('/dashboard')
            else:
                messages.error(request, 'Incorrect Credentials')
                return redirect('/dashboard')
        else:
            messages.error(request, 'Incorrect Credentials')
            return redirect('/dashboard')

def register(request):
    errors = Users.objects.Pass_validator(request.POST)
    if len(errors) > 0:
        for (key, value) in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        print(request.POST['password1'])
        passw = request.POST['password1']
        pw_hash = bcrypt.hashpw(passw.encode(), bcrypt.gensalt())
        print(pw_hash)
        Users.objects.create(email=request.POST['email'], password=pw_hash, first_name=request.POST['first_name'], last_name=request.POST['last_name']) 
        return redirect("/login")




def dashboard(request):
    request.POST.clear
    if 'user' not in request.session:
        messages.error(request, 'No credentials please log in')
        return redirect('/login')
    else:
        context = {
            'user': Users.objects.get(id=request.session['user']),
            'jobs': Jobs.objects.exclude(users=Users.objects.get(id=request.session['user'])),
        }
        return render(request, 'login_handler/dashboard.html', context)




def logout(request):
    request.session.clear()
    return redirect('/')

def createjob(request):
    currentUser = Users.objects.get(id=request.session['user'])
    if request.method == "GET":
        context = {
            'user': currentUser,
        }
        return render(request, "login_handler/newjob.html", context)
    elif request.method == "POST":
        errors = Jobs.objects.validater(request.POST)
        if len(errors) > 0:
            for (key, value) in errors.items():
                messages.error(request, value)
            return redirect('/jobs/new')
        else:
            addsting = ''
            if 'other' in request.POST:
                addsting = addsting + f"{request.POST['other']}, "
            if 'Trivial' in request.POST:
                addsting = addsting + f"{request.POST['Trivial']}, "
            if 'Intermediate' in request.POST:
                addsting = addsting + f"{request.POST['Intermediate']}, "
            if 'Difficult' in request.POST:
                addsting = addsting + f"{request.POST['Difficult']}, "
            Jobs.objects.create(title=request.POST['title'], description=request.POST['description'], location=request.POST['location'], created_by=Users.objects.get(id=request.session['user']), catagory=addsting)
            Jobs.objects.last().users.add(currentUser)
            
                
            return redirect('/dashboard')

def join(request, id):
    currentUser = Users.objects.get(id=request.session['user'])
    Jobs.objects.get(id=id).users.add(currentUser)
    return redirect('/dashboard')

def unjoin(request, id):
    currentUser = Users.objects.get(id=request.session['user'])
    currentjob = Jobs.objects.get(id=id)
    currentjob.users.remove(currentUser)
    return redirect('/dashboard')

def editjob(request, id):
    currentUser = Users.objects.get(id=request.session['user'])
    if request.method == "GET":
        context = {
            'myjobs': currentUser.jobs.all(),
            'user': currentUser,
            'jobs': Jobs.objects.all(),
            'thisjob': Jobs.objects.get(id=id)
        }
        return render(request, "login_handler/editjob.html", context)
    elif request.method == "POST":
        errors = Jobs.objects.validater(request.POST)
        if len(errors) > 0:
            for (key, value) in errors.items():
                messages.error(request, value)
            return redirect(f'/jobs/edit/{id}')
        else:
            job = Jobs.objects.get(id=id)
            job.title = request.POST['title']
            job.description = request.POST['description']
            job.location = request.POST['location']
            job.save()
            return redirect('/dashboard')

def delete(request, id):
    Jobs.objects.get(id=id).delete()
    return redirect('/dashboard')

def renderme(request, id):
    currentUser = Users.objects.get(id=request.session['user'])
    currentjob = Jobs.objects.get(id=id)
    context = {
        'user': currentUser,
        'job': currentjob,
    }
    return render(request, 'login_handler/renderme.html', context)





