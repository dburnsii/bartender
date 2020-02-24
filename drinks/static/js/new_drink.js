$(document).ready( () => {
    $("#colorPicker").change((e) => {
        $(".drink-header").css("background-image", `linear-gradient(${e.target.value}, white)`);
    });

    $("#colorPicker").spectrum({
        color: "#005aff",
        preferredFormat: "hex"
    });

    $("#colorPicker").spectrum("set", "#005aff");
    $("#colorPicker").change();

    var suggestions = [];
    var tempObj = {};
    var waiting;
    var saved_value;

    appendIngredient();


    $("#id_image").change((e) => {
        if(e.target.files && e.target.files[0]){
            var reader = new FileReader();
            reader.onload = function(e) {
                $(".drink-thumbnail").attr("src", e.target.result);
            }
            reader.readAsDataURL(e.target.files[0]);
        }
    });

    $("#ingredient_type_form").on('submit', (e) => {
        e.preventDefault();
        data = $(e.target).serializeArray()
        $.ajax({
            url: '/ingredient_types/',
            type: 'POST',
            data: data,
            success: () => {
                console.log("Success!");
                $("#ingredientModal").modal("hide");
                new_name = data.find((x) => x.name == "name").value;
                ingredient_types.push(new_name);
                waiting.value = new_name;
                $(waiting).change();
                waiting = null;
            },
            error: (xhr, errmsg, err) => {
                console.log("Failure!");
                console.log(errmsg);
            }
        });
    });

    function updateSuggestions() {
        suggestions.forEach((sugg) => {
            sugg.update(ingredient_types);
        });
    }

    function updateIngredients() {
        var ingredientNames = $.map($(".ingredient-name"), (e) => e.value);
        var ingredientQuantities = $.map($(".ingredient-quantity"), (e) => parseFloat(e.value) );
        var updatedIngredients = {};
        ingredientNames.forEach((key, i) => {
            if(key && ingredientQuantities[i] ){
                updatedIngredients[key] = ingredientQuantities[i];
            }
        });
        console.log(updatedIngredients);
        $("#id_ingredients").val(JSON.stringify(updatedIngredients));
    }

    function appendIngredient() {
        // Create new ingredient type row
        var item = $("<li></li>").addClass("list-group-item");
        var row = $("<div></div>").addClass("row ingredient-row");
        var nameDiv = $("<div></div>").addClass("input-group col-sm-6 col-8 pr-1");
        var quantityDiv = $("<div></div>").addClass("input-group col-sm-4 col-4 pl-1");
        var nameInput = $("<input type=\"text\" placeholder=\"Search\">").addClass("form-control ingredient-name")
        nameDiv.append(nameInput);
        var quantityInput = $("<input type=\"number\" step=\"0.1\" value=\"0.0\">").addClass("form-control px-2 ingredient-quantity");
        quantityDiv.append(quantityInput);
        var unitsDiv = $("<div></div>").addClass("input-group-append");
        unitsDiv.append($("<span>OZ</span>").addClass("input-group-text"));
        quantityDiv.append(unitsDiv);
        row.append(nameDiv);
        row.append(quantityDiv);
        item.append(row);

        var sugg = new Suggestions(nameInput[0], ingredient_types, { minLength: 1 });
        sugg.list.element.classList += " dropdown-menu";
        suggestions.push(sugg);
        nameInput.keyup(sugg, (e) => {
            console.log(e.data);
            if(e.data.query && e.data.list.isEmpty()){
                console.log("Empty!");
                empty = {
                    original: "New...",
                    string: "New..."
                };
                //e.data.list.items.add;
                e.data.list.drawItem(empty, true);
                e.data.list.show();

            }
        });
        //TODO: Make sure "new" shows up after selecting it the first time
        //TODO: Make sure modal updates ingredients variable
        //TODO: Make sure ingredients value update also updates sugg array
        //TODO: Create a way to remove from list

        nameInput.change((e) => {
            if(e.target.value === "New..."){
                e.target.value = "";
                waiting = e.target;
                $("#ingredientModal input#id_name").val(saved_value);
                $("#ingredientModal").modal();

            } else if(ingredient_types.includes(e.target.value)){
                //TODO: Prevent same ingredient from being added twice
                console.log("Added " + e.target.value);
                $(e.target).removeClass("is-invalid");
                updateIngredients();
                var quantity = $(e.target).parents(".ingredient-row").find(".ingredient-quantity")
                quantity.val("");
                quantity.focus();
                //TODO: Check if the length is >= than 10
                appendIngredient();
                //TODO: Animate this append
            } else if(!e.target.value){
                $(e.target).removeClass("is-invalid");
            } else {
                saved_value = $(e.target).val();
                $(e.target).addClass("is-invalid");
            }
        });

        quantityInput.change(() => {
            updateIngredients();
        });

        $("#ingredient-list").append(item);
    }

    //new Suggestions($("#ingredient_form_type")[0], ingredient_types, { minLength: 1, emptyText: "New..."});
    //suggestions.push(sugg);
});
