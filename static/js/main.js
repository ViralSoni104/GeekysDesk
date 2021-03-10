function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
var site_host = location.protocol + "//" + location.hostname + ":8000";

function Subscribe() {
    $.ajax({
        type: "POST",
        url: site_host +"/subscribe-to-newsletter/",
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'email': document.getElementById('subscribe_email').value
        },
        dataType: 'json',
        beforeSend: function () {
            $('#MSG').html('');
            $('#close').hide();
            $('#MSG').removeAttr('class');
            $('#subscribe_btn').removeClass('fab fa-telegram-plane');
            $('#subscribe_btn').addClass('fa fa-circle-o-notch fa-spin');
            $('#Subscribe').prop('disabled', true);
        },
        success: function (data) {
            $('#Subscribe').prop('disabled', false);
            $('#subscribe_btn').removeClass('fa fa-circle-o-notch fa-spin');
            $('#subscribe_btn').addClass('fab fa-telegram-plane');
            $('#MSG').addClass(data.class);
            $('#MSG').html(data.msg);
            $('#close').show();
        }
    });
}
function close_message() {
    $(".alert").alert('dispose');
    $('#close').hide();
    $('#MSG').removeClass('show');
    $('#MSG').html('');
    document.getElementById('subscribe_email').value = '';
}
var toasted = new Toasted({
    position : 'bottom-center',
    theme : 'primary',
    duration:5000,
    className:'toastClass',
    fullWidth:true,
})
function save_post(Post_to_Save,Bookmark_Class,reload_page=''){
    $.ajax({
            type: "POST",
            url: site_host + "/bookmark/",
            data: {
                'csrfmiddlewaretoken': getCookie('csrftoken'),
                'post_to_save':Post_to_Save,
            },
            dataType: 'json',
            beforeSend: function () {
                
            },
            success: function (data) {
            toasted.show("<span class='toast-content'><span class='fa fa-check-circle' style='color:#55efc4;font-size:18px;'></span>&nbsp;&nbsp;"+data.msg+"<span>");
            if(data.bookmarked)
            {
                $(Bookmark_Class).addClass('fa-bookmark');
                $(Bookmark_Class).removeClass('fa-bookmark-o');
                $('.saved_text').html('In Bookmarked');
                $('.saved_text').addClass('text-blue');
            }
            else{
                $(Bookmark_Class).addClass('fa-bookmark-o');
                $(Bookmark_Class).removeClass('fa-bookmark');
                $('.saved_text').html('Bookmark Post to read later');
                $('.saved_text').removeClass('text-blue');
            }
            $.ajax({
                type: "POST",
                url: site_host + "/updateCount/",
                data: {
                    'csrfmiddlewaretoken': getCookie('csrftoken'),
                    'post_to_save':Post_to_Save,
                },
                dataType: 'json',
                beforeSend: function () {
                    
                },
                success: function (data) {
                     $(Bookmark_Class+"_count").html(data);
                }
            });
            if(reload_page=='reload_page'){
                location.reload();
            }
        }
    });
}