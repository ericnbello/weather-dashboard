function toggleInterval(interval) {
    const daily = document.getElementsByClassName("daily");
    const hourly = document.getElementsByClassName("hourly");

    for (var i = 0; i < daily.length; i++) {
        if(interval==="daily"){
            daily[i].style.display = "flex";
            hourly[i].style.display = "none";
        }
        else {
            hourly[i].style.display = "flex";
            daily[i].style.display = "none";
        }
    };
};