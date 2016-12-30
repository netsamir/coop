$(document).ready(function(){
  $("#check_mycoop").click(function(event){
    event.preventDefault();
    $.getJSON("http://localhost:9000/mycoop",
      function(data){
        $('#collect_eggs').text(data[0].data);
        $('#chicken_message').text(data[0].message);
        $('#total_eggs').text(data[1].data);
        $('#chicken_message2').text(data[1].message);
      });// end getJSON
  });// end click
});
