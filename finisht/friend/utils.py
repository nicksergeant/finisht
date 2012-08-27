from django.contrib.auth.models import User
from finisht.friend.models import Friend

def are_friends(user1, user2):
    primary_friend = Friend.objects.filter(main_user=user1, friend_user=user2, pending=False)
    secondary_friend = Friend.objects.filter(main_user=user2, friend_user=user1, pending=False)
    if primary_friend or secondary_friend:
        return True
    else:
        return False
        
def are_pending_friends(user1, user2):
    primary_friend = Friend.objects.filter(main_user=user1, friend_user=user2, pending=True)
    secondary_friend = Friend.objects.filter(main_user=user2, friend_user=user1, pending=True)
    if primary_friend or secondary_friend:
        return True
    else:
        return False

def get_friends(id):
    friends = []
    friends_users = []
    primary_friends = Friend.objects.filter(main_user=id, pending=False)
    secondary_friends = Friend.objects.filter(friend_user=id, pending=False)
    for pfriend in primary_friends:
        friends.append(pfriend.friend_user.id)
    for sfriend in secondary_friends:
        friends.append(sfriend.main_user)
    for friend in friends:
        friends_users.append(User.objects.get(id=friend))
    return friends_users

def get_enemies(id):
    my_friends = get_friends(id)
    friend_iter = str(id)

    if len(my_friends) > 0:
        for friend in my_friends:
            friend_iter = friend_iter + ',' + str(friend.id)
    enemies = User.objects.extra(where=['id NOT IN (' + friend_iter + ')']).order_by('username')
    
    new_enemies = []
    for enemy in enemies:
        if not are_pending_friends(enemy.id, id):
            new_enemies.append(enemy)
    return new_enemies
