from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.db.models import Q

from finisht.forms import *

# Friends related import
from finisht.friend.models import Friend
from finisht.friend.forms import FriendForm
from finisht.friend.utils import are_friends, are_pending_friends
from finisht.friend.utils import get_friends, get_enemies

# Success related import
from finisht.success.forms import SuccessForm
from finisht.success.models import Success

import datetime
import inspect

def signup(request):
    signup_form = UserCreationForm(request.POST)
    if signup_form.is_valid():
        signup_form.save()
        user = authenticate(username=request.POST['username'], password=request.POST['password1'])
        auth_login(request, user)
        return HttpResponseRedirect('/')
    else:
        return render_to_response("signup.html", {
            'signup_form' : signup_form,
            'signup' : True,
            'data': request.POST
        })

def home(request):
    if request.user.is_authenticated():
        
        done_form = SuccessForm(request.POST)
    
        if done_form.is_valid():
            done_form = done_form.save(commit=False)
            done_form.user = request.user
            done_form.save()
            return HttpResponseRedirect('/?thanks')
        
        feedback_form = FeedbackForm(request.POST)
    
        if feedback_form.is_valid():
            message = request.user.username + ': ' + request.POST['message']
            send_mail('Finisht feedback', message, request.user.email, ['nick@nicksergeant.com'])
            return HttpResponseRedirect('/?thanks')
        
        my_friends = get_friends(request.user.id)
        friend_iter = str(request.user.id)
    
        if len(my_friends) > 0:
            for friend in my_friends:
                friend_iter = friend_iter + ',' + str(friend.id)
    
        successes = Success.objects.extra(where=['user_id IN (' + friend_iter + ')']).order_by('-completed_on')
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(1)
        last_month = datetime.datetime.now().month - 1
        this_year = datetime.datetime.now().year
        last_year = datetime.datetime.now().year - 1
    
        if last_month == 0:
            last_month = 12
            this_year = last_year + 1

        successes_today = successes.filter(completed_on__gte=today)
        successes_yesterday = successes.filter(completed_on__gte=yesterday, completed_on__lte=today)
        successes_this_week = successes.filter(completed_on__gte=today - datetime.timedelta(7))
        successes_this_month = successes.filter(completed_on__month=datetime.datetime.now().month, completed_on__year=this_year)
        successes_last_month = successes.filter(completed_on__month=last_month, completed_on__year=this_year)
    
        i = 0
        for success in successes_today:
            if success.user_id != request.user.id:
                successes_today[i].friend = True
            i += 1
    
        i = 0
        for success in successes_yesterday:
            if success.user_id != request.user.id:
                successes_yesterday[i].friend = True
            i += 1
    
        i = 0
        for success in successes_this_week:
            if success.user_id != request.user.id:
                successes_this_week[i].friend = True
            i += 1
    
        i = 0
        for success in successes_this_month:
            if success.user_id != request.user.id:
                successes_this_month[i].friend = True
            i += 1
    
        i = 0
        for success in successes_last_month:
            if success.user_id != request.user.id:
                successes_last_month[i].friend = True
            i += 1
        
        if len(my_friends) > 0:
            has_friends = True
        else:
            has_friends = False
    
    home = True
    
    disable_friends = request.session.get('disable_friends')
    
    developer_count = User.objects.count()
    success_count = Success.objects.count()
    return render_to_response('home.html', locals(), context_instance=RequestContext(request))

@login_required
def friends(request):
    friend_form = FriendForm(request.POST)

    if friend_form.is_valid():
        friend_form = friend_form.save(commit=False)
        if friend_form.friend_user.username != request.user.username:
            existing = Friend.objects.filter(main_user=friend_form.friend_user.id, friend_user=request.user.id)
            if not existing:
                existing = Friend.objects.filter(friend_user=friend_form.friend_user.id, main_user=request.user.id)
                if not existing:
                    friend_form.main_user = request.user.id
                    friend_form.pending = True
                    friend_form.save()
                    message = 'Hey there, ' + str(request.user.username) + ' wants to be your friend on finisht.com.  You can approve or deny this friend request by heading to http://finisht.com/friends/'
                    send_mail('Finisht friend request', message, 'no-reply@finisht.com', [friend_form.friend_user.email])
        return HttpResponseRedirect('/friends/')
    
    friend_list = Friend.objects.filter(Q(main_user=request.user.id) | Q(friend_user=request.user.id)).order_by('-friend_user')
    friends = True
    
    enemies = get_enemies(request.user.id)
    
    for friend in friend_list:
        if friend.main_user != request.user.id:
            friend.username = User.objects.get(id=friend.main_user).username
            friend.main_username = friend.username
        else:
            friend.username = friend.friend_user.username
    
    return render_to_response('friends.html', locals(), context_instance=RequestContext(request))

@login_required
def delete_success(request, id):
    byebye = Success.objects.get(id=id)
    if byebye.user_id == request.user.id:
        byebye.delete()
    return HttpResponseRedirect('/?thanks')

@login_required
def delete_friend(request, id):
    byebye = Friend.objects.get(id=id)
    byebye.delete()
    return HttpResponseRedirect('/friends/?sorry')

@login_required
def approve_friend(request, id):
    approve = Friend.objects.get(id=id)
    approve.pending = False
    approve.save()
    return HttpResponseRedirect('/friends/')
    
@login_required
def toggle_friends(request):
    if request.session.get('disable_friends') == True:
        request.session['disable_friends'] = False
        current_disable_state = False
    else:
        request.session['disable_friends'] = True
        current_disable_state = True
    return HttpResponse("{'current_disable_state': " + str(current_disable_state) + "}", mimetype='application/javascript')
