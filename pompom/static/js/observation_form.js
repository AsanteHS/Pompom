$(function () {

    var countCheckboxes = function (index, element) {
        var numberOfChecked = $(element).find(':checkbox:checked').length;
        var sectionID = $(element).data("section");
        $("#check-count-" + sectionID).val(numberOfChecked);
    };

    $('#observation-form').submit(function(event) {
        event.preventDefault();
        var el = $(this);
        $('.check-count-group').each(countCheckboxes);
        el.children('button').prop('disabled', true);
        el.unbind('submit').submit();
    });
});
