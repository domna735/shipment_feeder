document.addEventListener('DOMContentLoaded', function() {
  grecaptcha.ready(function() {
    var form = document.getElementById('formLogin');
    if(form) {
      form.addEventListener('submit', function(e) {
        e.preventDefault();
        grecaptcha.execute('6LcB8dcZAAAAAJO9mElsjCkPrWVj1rXr2SH9ML_h', {action: 'login'}).then(function(token) {
          var input = document.createElement('input');
          input.type = 'hidden';
          input.name = 'g-recaptcha-response';
          input.value = token;
          form.appendChild(input);
          form.submit();
        });
      });
    }
  });
});
