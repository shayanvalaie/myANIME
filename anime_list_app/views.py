from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . models import User, Anime
import bcrypt



# DISPLAY
def home(request):
    return render(request, 'home.html')
    
def index(request):
    if 'userid' in request.session: # <---- if i am logged in
        return redirect("/dashboard")
    # logic to stop users who are logged in from coming here
    return render(request, "index.html")

def dashboard(request):
    # Write code that blocks us from getting here
    # how do you know you are logged in or out
    # redirect to log in if i am not logged in
    if 'userid' not in request.session:
        return redirect('/')
    user_info= User.objects.get(id=request.session['userid']) 
    context = {
        "user_info" : user_info,
    }
    return render(request, "dashboard.html", context)

def create_page(request):
    user_info= User.objects.get(id=request.session['userid']) 
    all_users= User.objects.all()
    context = {
        "user_info" : user_info,
        "all_users" : all_users,
        
    }
    return render(request, "create.html", context)


def edit_page(request, id):
    # trip_info= Trip.objects.get(id=id)
    user_info = User.objects.get(id=request.session['userid'])
    context = {
        'anime_info' : Anime.objects.get(id=id),
        "user_info" : user_info,
    }
    

    return render(request, "edit.html", context)


def view_anime(request, id):
    user_info = User.objects.get(id=request.session['userid'])
    anime_info= Anime.objects.get(id=id)
    context = {
    "anime_info" : Anime.objects.get(id=id),
    "user_info" : user_info,
    }

    return render(request, "view_anime.html", context)
    

def editProfile(request, id):
    # trip_info= Trip.objects.get(id=id)
    user_info = User.objects.get(id=request.session['userid'])
    context = {
        "user_info" : user_info,
    }
    

    return render(request, "editProfile.html", context)












#ACTION

def register(request):
    print("test")
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/index")
    
    else:

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        user = User.objects.create(
            first_name=request.POST['fname'],
            last_name=request.POST['lname'],
            email=request.POST['email'],
            user_name=request.POST['user_name'],
            pfp=request.POST['pfp'],
            password=pw_hash,
            )
        # request.session['email'] = user.email
        # request.session['password'] = user.password
        request.session['userid'] = user.id
        return redirect("/dashboard")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/index")
    
    else:
        user = User.objects.filter(email=request.POST['email'])
        if user: 
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/dashboard')
        else:
            errors['email'] = 'no match for email'
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect("/index")
        return redirect('/index')


def create_new(request):
    
    errors = User.objects.create_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/anime/new")
    else:
        user = User.objects.get(id=request.session['userid'])
        if request.POST['end_date'] == '':
            new_anime= Anime.objects.create(
                title=request.POST['title'],
                start_date=request.POST['start_date'],
                season=request.POST['season'],
                episode=request.POST['episode'],
                rating=request.POST['rating'],
                user=user
            )
            return redirect('/dashboard')
        if request.POST['start_date'] == '':
            new_anime= Anime.objects.create(
                title=request.POST['title'],
                end_date=request.POST['end_date'],
                season=request.POST['season'],
                episode=request.POST['episode'],
                rating=request.POST['rating'],
                user=user
            )
            return redirect('/dashboard')
        if request.POST['start_date'] == '' and request.POST['end_date'] == '':
            new_anime = Anime.objects.create(
                title=request.POST['title'],
                season=request.POST['season'],
                start_date = request.POST['start_date'],
                end_date = request.POST['end_date'],
                episode=request.POST['episode'],
                rating=request.POST['rating'],
                user=user
            )
            return redirect('/dashboard')
            
        else:
            new_anime = Anime.objects.create(
                title=request.POST['title'],
                season=request.POST['season'],
                start_date=request.POST['start_date'],
                end_date=request.POST['end_date'],
                episode=request.POST['episode'],
                rating=request.POST['rating'],
                user=user
            )
            return redirect('/dashboard')


        return redirect('/dashboard')


def edit_anime(request, id):
    user = User.objects.get(id=request.session['userid'])
    errors = User.objects.create_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/anime/edit/{id}")
    
    else:
            


        if request.POST['end_date']:
            updated_anime = Anime.objects.get(id=id)
            updated_anime.title = request.POST['title']
            updated_anime.end_date = request.POST['end_date']
            updated_anime.season = request.POST['season']
            updated_anime.episode = request.POST['episode']
            updated_anime.rating = request.POST['rating']
            updated_anime.save()
            
            return redirect("/dashboard")

        if request.POST['start_date']:
            updated_anime = Anime.objects.get(id=id)
            updated_anime.title = request.POST['title']
            updated_anime.start_date = request.POST['start_date']
            updated_anime.season = request.POST['season']
            updated_anime.episode = request.POST['episode']
            updated_anime.rating = request.POST['rating']
            updated_anime.save()

            return redirect("/dashboard")




        if request.POST['end_date'] and request.POST['start_date']:
            updated_anime = Anime.objects.get(id=id)
            updated_anime.title = request.POST['title']
            updated_anime.start_date = request.POST['start_date']
            updated_anime.end_date = request.POST['end_date']
            updated_anime.season = request.POST['season']
            updated_anime.episode = request.POST['episode']
            updated_anime.rating = request.POST['rating']
            updated_anime.save()
            
            return redirect('/dashboard')

        if request.POST['start_date'] == "" and request.POST['end_date'] == "":
            updated_anime = Anime.objects.get(id=id)
            updated_anime.title = request.POST['title']
            updated_anime.season = request.POST['season']
            updated_anime.episode = request.POST['episode']
            updated_anime.rating = request.POST['rating']
            updated_anime.save()
            
            return redirect("/dashboard")

def editForm(request, id):
    user = User.objects.get(id=request.session['userid'])
    errors = User.objects.edit_user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/editProfile/{id}")
    else:
        updated_user =User.objects.get(id=id)
        if request.POST['user_name']:
            updated_user.user_name = request.POST['user_name']
            updated_user.save()
            return redirect('/dashboard')
        if request.POST['password']:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            updated_user.password = pw_hash
            updated_user.save()
        
            return redirect('/dashboard')

        if request.POST['user_name'] and request.POST['password']:
            updated_user.user_name = request.POST['user_name']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            updated_user.password = pw_hash
            updated_user.save()
            return redirect('/dashboard')

        if request.POST['user_name'] == '' and request.POST['password']=='':
            return redirect(f"/editProfile/{id}")


def delete_anime(request, id):
    user= User.objects.get(id=request.session['userid'])
    deleted_anime= Anime.objects.get(id=id)
    deleted_anime.delete()
    return redirect('/dashboard')
    




def logout(request): 
    del request.session['userid']

    return redirect('/index')



