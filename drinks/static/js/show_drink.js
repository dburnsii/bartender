


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
            { drink: JSON.stringify(selected_drink) },
            (data) => {
                console.log("Request sent.");
            }).done( (data) => {
                console.log(data);
            }).fail( (data) => {
                console.log(data);
            });
    });

});