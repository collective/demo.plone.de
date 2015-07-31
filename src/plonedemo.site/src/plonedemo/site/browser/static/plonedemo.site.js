
$(document).ready(function(){
    $('a.autologin').on("click", function(e) {
        e.preventDefault();
        var username = $(this).attr('data-autologin-user');
        var password = $(this).attr('data-autologin-password');
        $('input#__ac_name').click();
        $('input#__ac_name').val(username);
        $('input#__ac_password').click();
        $('input#__ac_password').val(password);
        // $('.formControls input[type="submit"]').show();
        $('.formControls input[type="submit"]').click();
    });
})
