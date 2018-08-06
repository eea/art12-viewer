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
