$.ajax({
  type: "GET",
  url: "{% url 'home' %}",
  success: function(data){
    alert( "Прибыли данные: ");
  }
});
