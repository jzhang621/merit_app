var submitNewRequest = function() {

  $('#submit-button').click( function(e) {
    e.preventDefault();
    var pledges = [],
      name,
      justification,
      suggestedValue;

    name = $('#name').val();
    justification = $('#justification').val();
    suggestedValue = $('#suggested-value').val();

    $('.pledge-checkbox').each( function() {
      if ($(this).is(':checked')) {
        pledges.push($(this).attr('pledge_id'));
      }
    });

    if (pledges.length == 0 || name == '') {
      alert('Please provide valid names');
      return;
    }

    $.ajax({
      url: '/commit_request',
      type: 'post',
      async: false,
      data: {
        'name': name,
        'justification': justification,
        'pledges': pledges.join(','),
        'suggestedValue': suggestedValue
      },
      dataType: 'html',
      beforeSend: function() {
        $('#message').hide();
        $('#message p').text('');
      },
      success: function(data) {
        $('#name').val('');
        $('#justification').val('');
        $('#suggested-value').val('');

        $('.pledge-checkbox').each( function() {
          $(this).attr('checked', false);
        });

        $('#message p').text(data);
        $('#message').show();
      }
    });

  });

};

