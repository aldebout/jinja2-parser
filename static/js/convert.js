$(document).ready(function(){
    $('#clear').click(function() {
        $('#jinja-template').val('');
        $('#jinja-render').val('');
        $('#jinja-values').val('');
        $('#jinja-render').html('');
        $('#jmespath-render').val('');
        $('#jmespath-render').html('');
    });

    $('#settings-btn').click(function() {
        $('#settings').toggle();
    });

    $('input[type=radio][name="use_case"]').change(function() {
        if ( this.value === "jinja" ) {
            $('#jinja-render-title').html("Render");
            $('.jmespath-class').hide();
        } else if ( this.value === "jmespath" ) {
            $('#jinja-render-title').html("JMESPath query");
            $('.jmespath-class').show();
        }
    });

    $('#convert-jinja').click(function() {
        var is_checked_showwhitespaces = $('input[name="showwhitespaces"]').is(':checked') ? 1:0;
        var is_checked_simulatesafe = $('input[name="simulatesafe"]').is(':checked') ? 1:0;

        console.log('Over here !');

        // Push the input to the Jinja2 api (Python)
        $.post('/convert', {
            jinja_template: $('#jinja-template').val(),
            jinja_values: $('#jinja-values').val(),
            jmespath_values: $('#jmespath-values').val(),
            showwhitespaces: is_checked_showwhitespaces,
            simulatesafe: is_checked_simulatesafe
        }).done(function(response) {
            // Display the answer
            console.log('I got something !');
            var response_object = JSON.parse(response);
            $('#jinja-render').html(response_object.jinja.replace(/•/g, '<span class="whitespace">•</span>'));
            $('#jmespath-render').html(response_object.jmespath.replace(/•/g, '<span class="whitespace">•</span>'));
        });
    });
});
