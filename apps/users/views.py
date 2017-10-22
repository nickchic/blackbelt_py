from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Friendship
import bcrypt

def index(request):
    return redirect('/main')

def main(request):
    context = {
        'logged_in':logged_in(request)
    }
    return render(request, 'users/index.html', context)

def login_action(request):
    if len(request.POST['password']) < 1 or len(request.POST['email']) < 1:
        return login_fail(request)

    try:
        user_to_check = User.objects.get(email=request.POST['email'])
    except User.DoesNotExist:
        return login_fail(request)

    password = request.POST['password'].encode("utf-8")

    if bcrypt.checkpw(password, user_to_check.password_hash.encode("utf-8")):
        request.session['id'] = user_to_check.id
        return redirect('/friends')
    else:
        return login_fail(request)

def login_fail(request):
    messages.error(request, "Login Failed")
    return redirect('/')

def register_action(request):
    errors = User.objects.user_validation(request.POST)
    print 'error len', len(errors)
    if len(errors) > 0:
        for tag, error in errors.iteritems():
            messages.error(request, error)
        return redirect('/')
    else:
        new_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print new_hash
        new_user = User(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password_hash=new_hash, dob=request.POST['dob'])
        new_user.save()
        request.session['id'] = new_user.id
        return redirect('/friends')

def get_logged_in_user(request):
    try:
        request.session['id']
    except KeyError:
        return None

    return User.objects.get(id=request.session['id'])

def logout(request):
    try:
        del request.session['id']
    except KeyError:
        pass
    return redirect('/')

def logged_in(request):
    if not get_logged_in_user(request) == None:
        return True
    else:
        return False

def user_page(request, user_id):
    if User.objects.id_exists(user_id):
        context = {
            'user':User.objects.get(id=user_id),
            'logged_in':logged_in(request)
        }
        return render(request, 'users/user.html', context)
    else:
        return redirect('/friends')

def friends(request):
    if logged_in(request):
        logged_in_user = get_logged_in_user(request)
        if logged_in_user.friends.count() == 0:
            has_friends = False
        else:
            has_friends = True
        context = {
            'logged_in_user': logged_in_user,
            'friends':logged_in_user.friends,
            'has_friends':has_friends,
            'others':User.objects.exclude(id__in=logged_in_user.friends.all()).exclude(id=logged_in_user.id)
        }
        return render(request, 'users/friends.html', context)
    else:
        return redirect('/main')

def user_home(request):
    if logged_in(request):
        return redirect('/users/{}'.format(get_logged_in_user(request).id))
    else:
        return redirect('/main')

def add_friend(request, user_id):
    if logged_in(request):
        Friendship.objects.create(friend_a_id=user_id, friend_b_id=get_logged_in_user(request).id)
        Friendship.objects.create(friend_a_id=get_logged_in_user(request).id, friend_b_id=user_id)
    return redirect('/friends')

def remove_friend(request, user_id):
    if logged_in(request):
        friendship_to_remove_a = Friendship.objects.get(friend_a_id=user_id, friend_b_id=get_logged_in_user(request).id)
        friendship_to_remove_a.delete()
        friendship_to_remove_b = Friendship.objects.get(friend_a_id=get_logged_in_user(request).id, friend_b_id=user_id)
        friendship_to_remove_b.delete()
    return redirect('/friends')
