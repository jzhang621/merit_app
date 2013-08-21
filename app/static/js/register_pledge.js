var registerPledge = function() {

  $('#submit-button').click( function(e) {
    e.preventDefault();
    var pledgeName,
      major,
      year;

    // TOOD: make sure that these are not empty
    pledgeName = $('#pledge-name').val();
    major = $('#major').val();
    year = $('#year').val();

    $.ajax({
      url: '/commit_pledge',
      type: 'post',
      async: false,
      data: {
        'pledgeName': pledgeName,
        'major': major,
        'year': year
      },
      dataType: 'html',
      beforeSend: function() {
        $('#commit-message div').remove();
      },
      success: function(data) {
        $('#commit-message').append(data);  
        $('#pledge-name').val('');
        $('#major').val('');
        $('#year').val('');
      },
      error: function(XHR, message) {
        $('#commit-message').append(message);
      }
    });
  });

};

