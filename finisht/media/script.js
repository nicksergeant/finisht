var activeLogin = '';
var activeDone = 'today';

$(function() {
    $("a").click(function() {this.blur();});

    if (activeLogin != '') {
        active = $('#' + activeLogin.toLowerCase());
        $("#signup, #login").bind("click", function() { SwapLogin($(this).html()); return false; });

        $("#signup-form input:not(.submit), #login-form input:not(.submit), #done-form textarea").focus(function() { $(this).parent().addClass("focused") });
        $("#signup-form input:not(.submit), #login-form input:not(.submit), #done-form textarea").blur(function() { $(this).parent().removeClass("focused") });
    }

    $('#no-problem').bind("click", function() { $(this).parent().css('display', 'none'); });
    
    $("#done-nav a").bind("click", function() {SwapDone($(this)); return false;});
    $('#done-list li a, #friends-list li a.delete').bind("click", function() {
        $(this).parent().css('background-color', '#F7D4D4');
        if (confirm("You sure you want to do that?")) { return true; }
        else { $(this).parent().css('background-color', '#EEEEEE'); return false; }
    });

    $('#done-list li:last-child').css('border-bottom', '1px solid #E5E5E5');
    $('#add-friend, #add-friend-link').click(function() { $('#add-friend-form').toggle(); });

    $('#friend-input').focus(function() { if ($(this).attr('value') == 'friend\'s username') { $(this).attr('value',''); } });

    $('#with-friends-check').bind('click', function() {
        $('#loading-friends').toggle()
        $.ajax({
            type: 'GET',
            url: '/toggle_friends/',
            success: function() {
                $('#loading-friends').toggle();
                $('.friend').toggle();
                if (hasFriends == true) {
                    if ($('#whats-done').html() == 'we\'ve') { $('#whats-done').html('I\'ve'); }
                    else { $('#whats-done').html('we\'ve'); }
                }
            }
        });
    });
    
    $('#id_description').focus();
});

function SwapLogin(current) {
    activeLoginLower = activeLogin.toLowerCase();
    currentLower = current.toLowerCase();
    $('#' + activeLoginLower + '-form').css('display', 'none');
    $('#' + currentLower + '-form').css('display', 'block');
    $('#' + activeLoginLower).replaceWith('<a href="/' + activeLoginLower + '/" id="' + activeLoginLower + '" onclick="SwapLogin(\'' + activeLogin + '\'); return false;">' + activeLogin + '</a>');
    $('#' + currentLower).replaceWith('<span id="' + currentLower + '" onclick="SwapLogin(\'' + current + '\'); return false;">' + current + '</span>');
    activeLogin = current;
    return false;
}

function SwapDone(current) {
    current = current.html().toLowerCase().replace(' ','').replace(' ','');
    if (current != activeDone) {
        $('#' + current + '-nav').addClass('active');
        $('#' + activeDone + '-nav').removeClass('active');
        $('#' + current).css('display', 'block');
        $('#' + activeDone).css('display', 'none');
        $('#' + current.toLowerCase().replace(' ','')).css('display','block');
        activeDone = current;
        return false;
    } else {
        return false;
    }
}