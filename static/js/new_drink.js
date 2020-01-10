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
});
