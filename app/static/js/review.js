var approveRequests = function() {
  $('#submit-button').click( function() {
    var approved = {},
      rejected = [],
      request_id;

    $('.request').each( function() {
      input = $(this).find('input');
      request_id = input.attr('request-id'); 
      if (input.is(':checked')) {
        value = $('.value', this).text();
        approved[request_id] = value;
      } else {
        rejected.push(request_id); 
      };
    });

    $.ajax({
      url: '/approve_requests',
      type: 'post',
      async: false,
      dataType: 'json',
      data: {
        'approved': JSON.stringify(approved),
        'rejected': rejected.join(',')
      },
      success: function(data) {
        console.log('success');
      }
    });
  });
};

