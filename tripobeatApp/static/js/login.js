 $(document).ready(function () {
     $('#admin-radio').on('click', function(){
         var secretKeyField = document.querySelector('.secret-key-field');
         $('.secret-key-field').show();
     })

        $('#user-radio').on('click', function(){
        var secretKeyField = document.querySelector('.secret-key-field');
        $('.secret-key-field').hide();
    })
 });