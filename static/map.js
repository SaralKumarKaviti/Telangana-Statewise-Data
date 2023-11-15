document.addEventListener("DOMContentLoaded", function() {
    var districts = document.querySelectorAll(".district");
    
    // Add click event listener to each district
    districts.forEach(function(district) {
        district.addEventListener("click", function() {
            // Remove the "selected" class from all districts
            districts.forEach(function(district) {
                district.classList.remove("selected");
            });

            // Add the "selected" class to the clicked district
            this.classList.add("selected");
        });
    });
});
