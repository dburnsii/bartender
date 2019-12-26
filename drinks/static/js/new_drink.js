$(document).ready( () => {
    /*var select = document.getElementById("id_type");
    var option = document.createElement("option");
    var submit =  $('input[type="submit"]');
    option.text = "New...";
    option.value = "new";
    select.add(option);

    select.addEventListener("change", function() {
        if(select.value == "new")
        {
            console.log("New!");
            submit.attr("disabled", true);
            $("#categoryModal").modal();
        }
        else
        {
            console.log("Not new");
            submit.removeAttr("disabled");
        }
    });*/

    $("#colorPicker").spectrum({
        color: "#00aeef",
        preferredFormat: "hex"
    });

});
