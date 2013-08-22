var submitNewRequest = function() {

  $('#submit-button').click( function(e) {
    e.preventDefault();
    var name, 
      justification,
      pledgeName,
      type,
      value;

    name = $('#name').val();
    justification = $('#justification').val();
    pledgeName = $('#pledge-name').val();
    type = $('#type').val();
    suggestedValue = $('#suggested-value').val();

    if (pledgeName == '' || name == '') {
      alert('Please provide valid names');
    }

    //TODO ensure that pledgeName is one of the valid pledgeNames 

    $.ajax({
      url: '/commit_request',
      type: 'post',
      async: false,
      data: {
        'name': name,
        'justification': justification,
        'pledgeName': pledgeName,
        'type': type,
        'suggestedValue': suggestedValue
      },
      dataType: 'html',
      success: function() {
        $('#name').val('');
        $('#justification').val('');
        $('#pledge-name').val('');
        $('#type').val('');
        $('#suggested-value').val('');
      } 
    });
    
  });

};

var registerAutoComplete = function() {

  var pledges = [
    'Albert Hu',
    'Amy Chiang',
    'Andre King',
    'Betty Hu',
    'Chris Santiago',
    'Daniel Kang',
    'Gabe Kauffman',
    'Julia Li',
    'Kai Li',
    'Ling Yeung',
    'Matt Chiang',
    'Nicole Amira'
  ];

  $('#pledge-name').autocomplete({
    source: pledges
  });

};
