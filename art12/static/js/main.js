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
        var data = {'dataset_id': value};
        var url = '/summary/filter_form';
        $.ajax({
            type: "GET",
            url: url,
            data: data,
            dataType: 'html',
            success: function(resp) {
                var data = JSON.parse(resp);
                $('#subject').empty();
                $.each(data, function(index, element) {
                    console.log(element);
                    $('#subject').append(
                        $("<option></option>")
                            .text(element[1])
                            .val(element[0])
                    );
                });
            },
            error: function(resp) {
                alert('Error on selection')
            }
        });
    });

    $('.copy-disabled').bind('contextmenu', function(e){
        return false;
    });

    var ctrlDown = false;
    var ctrlKey = 17, aKey=65, cKey = 67, vKey = 86;

    $(document).keydown(function(e){
        if (e.keyCode == ctrlKey) ctrlDown = true;
    }).keyup(function(e){
        if (e.keyCode == ctrlKey) ctrlDown = false;
    });

    $('.copy-disabled').bind('keydown', (function(e) {
        if (ctrlDown && (e.keyCode == vKey || e.keyCode == cKey || e.keyCode == aKey))
            return false;
    }));
});
