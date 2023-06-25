document.getElementById('h3_user').addEventListener('click', function() {
    var user_options = document.getElementById('user_options');
    var user=document.getElementById('h3_user')
    if (user_options.style.display === "none") {
        user_options.style.display = "flex";
        user_options.style.flexDirection = "column";
        user_options.style.justifyContent = "center";
        user_options.style.alignItems = "center";
        
      } else {
        user_options.style.display = "none";
      }
})

