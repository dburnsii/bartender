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

    /*$(".ingredient-name").keyup((event) => {
        if(suggestions.list.items.length == 0){
            var temp = document.createElement('li');
            temp.appendChild(document.createTextNode('New...'));
            temp.addEventListener('click', () => {console.log("test")});
            suggestions.list.element.appendChild(temp);
            suggestions.list.element.style.display = "block";
            $(".suggestions li").click((e) => {
                console.log("test");
            });
        }

    });

    $(".suggestions").click((event) => {
        console.log("Click");
        console.log(event.target);
    })*/



});
