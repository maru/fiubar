/* Hide help texts when loading page */
$('div.help_text').css({ display: 'none' });

if ($('#id_request_auth').html().length == 0 && $('#id_tipo_request_auth').val() != 'o') {
	$('#id_request_auth').css({ display: 'none' });
}

$(document).ready(function(){

	/* Show and hide help texts */
    $('#id_username').focus(function () { $('#help_username').css({ display: 'block' }); });
    $('#id_username').blur (function () { $('#help_username').css({ display: 'none'  }); });

    $('#id_verificacion').focus(function () { $('#help_verificacion').css({ display: 'block' }); });
    $('#id_verificacion').blur (function () { $('#help_verificacion').css({ display: 'none'  }); });

    $('#id_first_name').focus(function () { $('#help_first_name').css({ display: 'block' }); });
    $('#id_first_name').blur (function () { $('#help_first_name').css({ display: 'none'  }); });

    $('#id_last_name').focus(function () { $('#help_last_name').css({ display: 'block' }); });
    $('#id_last_name').blur (function () { $('#help_last_name').css({ display: 'none'  }); });

    $('#id_email').focus(function () { $('#help_email').css({ display: 'block' }); });
    $('#id_email').blur (function () { $('#help_email').css({ display: 'none'  }); });

    $('#id_password').focus(function () { $('#help_password').css({ display: 'block' }); });
    $('#id_password').blur (function () { $('#help_password').css({ display: 'none'  });
		if ($('#id_password').val().length < 6) { $('#password_status').attr('class', 'status-error'); }
	});

    $('#id_password_verify').focus(function () { $('#help_password_verify').css({ display: 'block' }); });
	$('#id_password_verify').blur (function () { $('#help_password_verify').css({ display: 'none'  });
        /** Check passwords **/
        if ($('#id_password_verify').val() == $('#id_password').val()) {
            if ($('#id_password').val().length >= 6) {
			  $('#password_status').attr('class', 'status-correct');
              $('#password_verify_status').attr('class', 'status-correct');
            }
        } else {
			$('#password_status').attr('class', 'status-error');
            $('#password_verify_status').attr('class', 'status-error');
        }
    });

    $('#id_tipo_request_auth').change(function () {
        if ($('#id_tipo_request_auth').val() == 'o') {
          $('#id_request_auth').css({ display: 'block' });
        }
    });
    $('#id_tipo_request_auth').blur(function () {
        if ($('#id_tipo_request_auth').val() == 'o') {
          $('#id_request_auth').css({ display: 'block' });
        }
    });

	/* Shows textarea when option 'o' is chosen */
	function show_request_auth() {
		$('#id_tipo_request_auth').val('o');
		$('#id_request_auth').css({ display: 'block' });
	}

});

