$(document).ready( function() {

    $(".form_div").submit( function(e) {
        var token = $("#access_token").val();
        if (token == "") {
            e.preventDefault();
            $("#access_token").addClass("form-control-warning");
            alert("Enter an Access Token");
        } else {
            $("<input />").attr("type", "hidden").attr("name", "access_token").attr("value", token).appendTo(this);
        }
        var form = document.getElementById(this.id).elements;
        for (var i=0; i<form.length; i++) {
            if (form[i].classList.contains("required")) {
                if (form[i].value == "" && $(form[i]).prop("disabled") != true) {
                    e.preventDefault();
                    if ($("#"+form[i].id+"_alert_msg").length == 0 ) {
                        var alert = "<br><div id='"+form[i].id+"_alert_msg' "
                        +"class='alert alert-danger'><strong>Submission Error!</strong> You left a required field "
                        +form[i].id+" empty!</div>";
                        $("#"+form[i].id).css("border", "4px solid red");
                        $("#"+form[i].id+"_alert").append(alert);
                    }

                if ($(form[i]).attr("data-group") == "bulk") {
                    console.log($(form[i]).attr("data-pair"));
                }
                }
            }
        }
    });

    $(document).on("click", ".id_select", function() {
        var data_pair = $(this).attr("data-pair");
        var data_group = $(this).attr("data-group");
        var group = document.querySelectorAll("[data-group='"+data_group+"']");
        for (i=0; i<group.length;i++) {
            if ($(group[i]).attr("data-pair") != data_pair) {
                if ($(group[i]).attr("type") == "text") {
                    $(group[i]).prop("disabled", true);
                }
            } else {
                $(group[i]).attr("disabled", false);
                $(group[i]).prop("checked", true);
            }
        }
    });
    $(document).on("click", "#interval_select", function() {
        if ($("#interval_select").prop("checked")) {
            $(".interval_select_input").prop("disabled", false);
            $(".interval_select_input").addClass("required");
        } else {
            $(".interval_select_input").prop("disabled", true);
            $(".interval_select_input").removeClass("required");
            $(".interval_select_input").css("border", "none");
        }
    });
    $(document).on("click", "#meter_select", function() {
        if ($("#meter_select").prop("checked")) {
            $(".meter_select_input").prop("disabled", false);
            $(".meter_select_input").addClass("required");
        } else {
            $(".meter_select_input").prop("disabled", true);
            $(".meter_select_input").removeClass("required");
            $(".meter_select_input").css("border", "none");
        }
    });

    $(document).on("click", "#toggle_xml", function() {
        $("#xml_div").toggle();
    });
});