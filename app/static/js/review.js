var approveRequests = function() {
  $('#submit-button').click( function(e) {
    e.preventDefault();

    var approved = {},
      rejected = [],
      save,
      approve,
      request,
      request_id;

    $('.request').each( function() {
      request_id = $(this).attr('request-id'); 

      // begin check to see what action to take on request
      save = $(this).find('.save').is(':checked');
      if (save) {
        return true;
      }

      approve = $(this).find('.approve').is(':checked');
      if (approve) {
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
        data.success.forEach( function(entry) {
          $('tr[request-id=' + entry + ']').remove();
        });
      }
    });
  });
};

