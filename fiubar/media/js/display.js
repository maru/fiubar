$(document).ready(function(){

    /* Hide user messages after 5000 milliseconds. */
    setInterval(hideUserMessages, 5000);
    function hideUserMessages() {
      if (ul = $('div.user-messages')) {
          ul.fadeOut('normal');
      }
      return false;
    }

	/* Validate comments */
    $("form#commentform").submit(function() {
	  if ($('#comment').val().length <= 0) {
		$('span#comment-error').css({ 'display' : 'inline'});
		return false;
	  }
	  return true;
    });

    /* profiles/photo_form.html
    $('.photo-tab-delete').hover(
      function () {
        id = $(this).children('input').val();
        $('#' + id + ' img').addClass('photo-image-hover');
        $(this).children('a').children('img').attr({ 'src' : '/media/images/delete.png' });
      },
      function () {
        id = $(this).children('input').val();
        $('#' + id + ' img').removeClass('photo-image-hover');
        $(this).children('a').children('img').attr({ 'src' : '/media/images/delete_gray.png' });
      }
    );*/
});

/**
 *  Send bug ajax function.
 */
$(function() {
  $('#sidebar-bugs').submit(function() {
    var inputs = [];
    $(':input', this).each(function() {
      if (this.name != 'submit') {
        inputs.push(this.name + '=' + escape(this.value));
      }
    });

    ret = jQuery.ajax({
      type: 'POST',
      url: '/about/bugs/',
      data: inputs.join('&'),
      error: function (XMLHttpRequest, textStatus, errorThrown) {
        $('div.sidebar-content').html('\
          <div class="bugs-error">\
          <span class="error">AUCH!<br />Error al mandar el error!</span><br />\
          Por favor, andá a <a href="">esta página</a>.\
          </div>');
      },
      success: function(text) {
        $('div.sidebar-content').html('\
          <p class="bugs-thankyou">\
            &iexcl;Gracias por tu contribuci&oacute;n!<br />\
            <img src="/media/images/about/bugs-thankyou1.jpg" alt="" />\
            Tu error fue mandado.<br />\
            Nos ocuparemos de este problema apenas podamos.<br />\
          </p>');
      }
    });
    return false;
  });
});

/**
 * Messages app javascript functions
 * @maru Oct.2007
 */

    /**
     * Shows reply form
     */
    function reply_message() {
        form = document.getElementById('inbox-reply');
        if (form.style.display != 'block') {
            form.style.display = 'block';
        } else {
            form.style.display = 'none';
        }
    }

    /**
     * Selects all messages
     */
    function msg_select_all() {
        tick_msgs = document.getElementsByName('msg_id');

        link_all = document.getElementById('select-all-link');
        link_none = document.getElementById('select-none-link');

        link_all.style.display = 'none';
        link_none.style.display = 'block';

        for (i = 0; i < tick_msgs.length; i++) {
            tick_msgs[i].checked = true;
        }
        return false;
    }

    /**
     * Shows reply form
     */
    function msg_deselect_all() {
        tick_msgs = document.getElementsByName('msg_id');
        msg_state = !tick_msgs[0].checked;

        link_all = document.getElementById('select-all-link');
        link_none = document.getElementById('select-none-link');

        link_all.style.display = 'block';
        link_none.style.display = 'none';

        for (i = 0; i < tick_msgs.length; i++) {
            tick_msgs[i].checked = false;
        }
        return false;
    }

    /**
     * Checks if user is Ok to delete!
     */
    function check_delete(text) {
        return confirm(text);
    }

/**
 * Groups app javascript functions
 * @maru Dec.2007
 */

    /**
     * Shows reply form
     */
    function show_advopt() {
        form = document.getElementById('create-group-advanced');
        link = document.getElementById('show-advanced-options');

        form.style.display = 'block';
        link.style.display = 'none';

        link = document.getElementById('hide-advanced-options');
        link.style.display = 'inline';

        return false;
    }

    /**
     * Hides reply form
     */
    function hide_advopt() {
        form = document.getElementById('create-group-advanced');
        link = document.getElementById('show-advanced-options');

        form.style.display = 'none';
        link.style.display = 'inline';

        link = document.getElementById('hide-advanced-options');
        link.style.display = 'none';
    }

    /**
     * Selects/Deselects all members
     */
    function member_select_all() {
        check_all = document.getElementById('member_check_all');
        tick_members = document.getElementsByName('member');

        for (i = 0; i < tick_members.length; i++) {
            tick_members[i].checked = check_all.checked;
        }
        return false;
    }

    /**
     * Checks if user is Ok to unsubscribe!
     */
    function check_unsubscribe(text) {
        return confirm(text);
    }

$(document).ready(function(){

  $('li.materia-event').hover(function () {
    if ($(this).find('a.event-delete')) {
      $(this).find('a.event-delete').css({ 'display' : 'inline'});
    }
  }, function () {
    if ($(this).find('a.event-delete')) {
      $(this).find('a.event-delete').css({ 'display' : 'none' });
    }
  });
/*
   function cargar_cursos() {
      cuatrimestre = $('select#id_cursada_cuat option:selected');
      year = $('select#id_cursada_year option:selected');
      if (cuatrimestre.val() != '' && year.val() != '0') {
         ret = jQuery.ajax({
            type: 'POST',
            url: '/facultad/materias/',
            data: 'xhr&cuat=' + cuatrimestre + '&year=' + year,
            error: function (XMLHttpRequest, textStatus, errorThrown) {
               $('div.sidebar-content').html('');
            },
            success: function(text) {
               $('div#materia_cursos').html('<label class="cursada">Curso</label> ' + text);
            }
         });
      }
   }
   $('select#id_cursada_cuat').change(function () {
      cargar_cursos();
   }).change();
   $('select#id_cursada_year').change(function () {
      cargar_cursos();
   }).change();
*/
});


