function unitInterval(unit_system) {
    const imperial = document.getElementsByClassName("imperial");
    const metric = document.getElementsByClassName("metric");

    for (let i = 0; i < imperial.length; i++) {
        if(unit_system==="imperial"){
            imperial[i].style.display = "flex";
            metric[i].style.display = "none";
        }
        else {
            imperial[i].style.display = "none";
            metric[i].style.display = "flex";
        }
    };
};