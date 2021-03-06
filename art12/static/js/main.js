// jQuery Power Tip
$(document).ready(function () {
    $(".complex_datatable td, .complex_datatable th").each(function () {
        var type = $(this).data('tooltip');
        var place = $(this).data('tooltip-place');
        if (place == undefined) {
            place = "sw-alt";
        }

        switch (type) {
            case 'mouseover':
                var tooltip = $(this).attr('title');
                if (tooltip) {
                    tooltip = tooltip.replace(/\n/g, '<br />');
                    $(this).data('powertip', tooltip);
                    $(this).powerTip({
                        placement: place,
                        smartPlacement: true,
                        mouseOnToPopup: true,
                        offset: 0,
                    });
                }
                $(this).removeAttr('title');
                break;

            case 'html':
                var br = $(this).find('.br').text();
                if (br != undefined) {
                    br = br.replace(/\n/g, '<br />');
                }
                var tooltip = $(this).find('.tooltip-html').html();
                $(this).data('powertip', tooltip);
                $(this).powerTip({
                    placement: place,
                    mouseOnToPopup: true,
                    offset: 0,
                });
                break;

            default:
                var tooltip = $(this).attr('title');
                if (tooltip) {
                    tooltip = tooltip.replace(/\n/g, '<br />');
                    $(this).data('powertip', tooltip);
                    $(this).powerTip({
                        placement: place,
                        smartPlacement: true,
                        offset: 0,
                    });
                    $(this).removeAttr('title');
                }
        }
    });
});

$(document).ready(function () {
    $('#period').on('change', function () {
        var option = $(this).find(':selected');
        var value = option.val();
        var subject_selected = $('#subject option:selected').val();
        $('#subject').data('subject', subject_selected);

        if ($('#subject')){
          var data = {'dataset_id': value};
          var url = $(this).data('href');
          $.ajax({
            type: "GET",
            url: url,
            data: data,
            dataType: 'html',
            success: function(resp) {
              var data = JSON.parse(resp);
              var subject_selected = $('#subject').data('subject');
              $('#subject').empty();
              $.each(data, function(index, element) {
                if (element[0] == subject_selected){
                  $('#subject').append(
                  $("<option selected></option>")
                    .text(element[1])
                    .val(element[0])
                  );
                }
                else{
                  $('#subject').append(
                  $("<option></option>")
                    .text(element[1])
                    .val(element[0])
                  );
                }
              });
            },
            error: function(resp) {
              alert('Error on selection')
            }
          });
        }

        var option = $(this).find(':selected');
        var value = option.val();
        var country_selected = $('#country').find(':selected').val();
        $('#country').data('country', subject_selected);
        var data = {'dataset_id': value};
        var url = $(this).data('href-countries');
        if ($('#country')){
        $.ajax({
            type: "GET",
            url: url,
            data: data,
            dataType: 'html',
            success: function(resp) {
                var data = JSON.parse(resp);
                $('#country').empty();
                $.each(data, function(index, element) {
                    var country_selected = $('#country').data('country');
                    if (element[0] == country_selected){
                      $('#country').append(
                        $("<option selected></option>")
                            .text(element[1])
                            .val(element[0])
                    );
                    }
                    else{
                    $('#country').append(
                        $("<option></option>")
                            .text(element[1])
                            .val(element[0])
                    );
                    }
                });
            },
            error: function(resp) {
                alert('Error on selection')
            }
        });
        }
    });

    $('#subject').on('change', function () {
        var option = $(this).find(':selected');
        var subject = option.val();
        var subject_selected = $('#subject option:selected').val();
        $('#subject').data('subject', subject_selected);

        if ($('#subject')){
          var data = {'dataset_id': $('#period').find(':selected').val(),
                      'subject': subject};
          var url = $(this).data('href');
          $.ajax({
            type: "GET",
            url: url,
            data: data,
            dataType: 'html',
            success: function(resp) {
              var data = JSON.parse(resp);
              var subject_selected = $('#reported_name').data('subject');
              $('#reported_name').empty();
              $.each(data, function(index, element) {
                if (element[0] == subject_selected){
                  $('#reported_name').append(
                  $("<option selected></option>")
                    .text(element[1])
                    .val(element[0])
                  );
                }
                else{
                  $('#reported_name').append(
                  $("<option></option>")
                    .text(element[1])
                    .val(element[0])
                  );
                }
              });
            },
            error: function(resp) {
              alert('Error on selection')
            }
          });
        }
    });

    var copy_alert = 'Copying the data is not allowed';
    $('.copy-disabled').bind('contextmenu', function(e){
        alert(copy_alert);
        return false;
    });

    var ctrlDown = false;
    var ctrlKey = 17, aKey=65, cKey = 67;

    $(document).keydown(function(e){
        if (e.keyCode == ctrlKey) ctrlDown = true;
    }).keyup(function(e){
        if (e.keyCode == ctrlKey) ctrlDown = false;
    });

    $('.copy-disabled').bind('keydown', (function(e) {
        if (ctrlDown && (e.keyCode == cKey || e.keyCode == aKey)){
            alert(copy_alert);
            return false;
        }
    }));
});


// Flash Messages
$(document).ready( function () {

    var msg = $('.flashmessage');

    var show_flash = function () {
        $(msg).addClass('show');
    }

    var hide_flash = function () {
        $(msg).removeClass('show');
    }

    window.setTimeout(show_flash, 600);
    window.setTimeout(hide_flash, 3600);

    $(msg).on('mouseenter', show_flash);

    $(msg).on('mouseleave', function () {
        window.setTimeout(hide_flash, 600);
    });
});

$(function() {
    $('.close-popup').on('click', function (evt) {
      evt.preventDefault();
      window.close();
    });

    $('body').on('click', '.popup-btn', function(evt) {
      evt.preventDefault();
      var link = $(this);
      var url = link.attr('href');
      var name = "Comments";
      var params = 'height=600,width=600,screenX=300,screenY=100,scrollbars=1';
      var popup = window.open(url, name, params);
      popup.focus();
    });


    $('body').on('click', '#show-eu-map', function (evt) {
        var url = $(this).data('url');
        if (url != "") {
            title = "EU map of population trend";
            var params = "left=400,top=100,width=510,height=880," +
                "toolbar=0,resizable=0,scrollbars=0";
            window.open(url, title, params).focus();
        }
    });

    $('body').on('click', '#wikibutton', function (evt) {
        evt.preventDefault();
        var button = $(this);
        var url = button.attr('href');
        var name = '';
        var params = 'height=600,width=600,screenX=300,screenY=100,scrollbars=1';
        var popup = window.open(url, name, params);
        popup.focus();

    });

    $('body').on('click', '#show-map', function(evt) {
        var url = $(this).data('url');
        if (url != "") {
            title = "Map";
            var params = "left=400,top=100,width=700,height=420," +
                            "toolbar=0,resizable=0,scrollbars=0";
            window.open(url, title, params).focus();
        }
    });
});


$(document).ready(function () {
  var popouts = $(".popout");
  var popoutButtons = $("[data-popout]");

  // Open popout
  $(popoutButtons).on('click', function (event) {
      event.stopPropagation();
      var similar = $(this).data('popout');
      var intendedTarget = $(this).closest('.popout-wrapper').find(".popout");
      if ( $(intendedTarget).hasClass('open') ) {
          $(intendedTarget).removeClass('open');
      } else {
          // $(".popout." + similar).removeClass('open'); // to close similar
          $(".popout").removeClass('open');
          $(intendedTarget).addClass('open');
      }
  });

  // Close popout
  $('.popout').on('click', '.close', function () {
      $(this).closest('.popout').toggleClass('open');
  });
  $('.popout').on('click', function (event) {
      event.stopPropagation();
  });
  $('html').on('click', function() {
      $(popouts).removeClass('open');
  });

  // Assesment
  $('.popout.assesment').each(function () {
      var method = $(this).find("select");
      var radios = $(this).find("input[type='radio']");
      var preview = $(this).closest('.popout-wrapper').find(".conclusion.select");
      var previewValue = $(preview).data('value');
      var prevSecondClick = $(radios).filter(':checked');
      var currentClass = $(preview).data('initial');

      var updateSelect = function () {
          if ($(this).val()) {
              $(preview).children('.selected-value').removeClass('hidden').html( $(this).val() );
          } else {
              $(preview).children('.selected-value').addClass('hidden').html( $(this).val() );
          }
      };

      var updateRadio = function (event) {
          event.stopPropagation();
          conclusionClass = $(this).data('class');
          // Match selected conclusion
          $(preview).removeClass(currentClass);
          if (currentClass != conclusionClass) {
              currentClass = conclusionClass;
              $(preview).addClass(currentClass);
          } else {
              currentClass = false;
              $(preview).removeClass(currentClass);
          }
          // Uncheck radio button
          var secondClick = $(this).attr('secondClick');
          if (secondClick == "false" || secondClick == undefined) {
              $(prevSecondClick).attr('secondClick', false);
              $(this).attr('secondClick', true);
          } else {
              $(this).attr('secondClick', false);
              this.checked = false;
          }
          // update value
          if (previewValue == 'radio') {
              var checked = $(radios).filter(':checked');
              if ($(checked).val())
                  $(preview).children('.selected-value').removeClass('hidden').html($(checked).val());
              else
                  $(preview).children('.selected-value').addClass('hidden').html('');
          }
          prevSecondClick = this;
      };

      // Value
      if (previewValue == 'method') {
          $(method).on('change', updateSelect);
      }

      // Radios
      $(radios).on('click', updateRadio);
  });
});
