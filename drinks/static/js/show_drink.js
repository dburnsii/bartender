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
var csrftoken = getCookie('csrftoken');    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(document).ready(() => {
    console.log(options);
    var selected_drink = {};

    $("#pour_button").click(() => {
        Object.keys(ingredients).forEach((ingredient, index) => {
            option = options[ingredient];
            if(!option){
                console.log(`Nothing available for ${ingredient}!!`);
                //return;
            } else if(option.length > 1) {
                console.log("TODO: Open a modal here to give the user a selection.");
                selected_drink[option[0]] = ingredients[ingredient];
            } else {
                selected_drink[option[0]] = ingredients[ingredient];
            }
        });
        console.log(selected_drink);
        $.post("/pour/",
            { drink: selected_drink },
            () => {
                console.log("Request sent.");
            }).done( () => {
                console.log("Request done.");
            }).fail( () => {
                console.log("Request failed.");
            });
    });

});