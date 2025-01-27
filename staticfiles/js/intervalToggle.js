function toggleInterval(interval) {

    // e.preventDefault();
    
    // const daily = document.getElementsByClassName("daily");
    const today = document.getElementsByClassName("today");
    const next48hours = document.getElementsByClassName("next48hours");
    const monthly = document.getElementsByClassName("monthly");
    const radar = document.getElementsByClassName("radar");
    const studyCard = document.getElementById("study-card");
    const alerts = document.getElementsByClassName("alerts");
    const trends = document.getElementsByClassName("trends");

    // dashboard cards
    const profileCard2 = document.getElementById("profile-card-2");
    const card1 = document.getElementById("card1");
    const card2 = document.getElementById("card2");
    const card3 = document.getElementById("card3");
    const card4 = document.getElementById("card4");
    const card5 = document.getElementById("card5");
    const card6 = document.getElementById("card6");
    const card7 = document.getElementById("card7");
    const card8 = document.getElementById("card8");

    for (var i = 0; i < today.length; i++) {
        if(interval==="today"){
            today[i].style.display = "flex";
            next48hours[i].style.display = "none";
            monthly[i].style.display = "none";
            // radar[i].style.display = "none";
            // alerts[i].style.display = "none";
            // trends[i].style.display = "none";
        }
        else if (interval==="next48hours") {
            next48hours[i].style.display = "flex";
            // next48hours[i].style.color = "white";
            today[i].style.display = "none";
            monthly[i].style.display = "none";
            // radar[i].style.display = "none";
            // alerts[i].style.display = "none";
            // trends[i].style.display = "none";
        }
        else if (interval==="monthly") {
            monthly[i].style.display = "flex";
            today[i].style.display = "none";
            next48hours[i].style.display = "none";
            // card8.style.display = "none";
            // radar[i].style.display = "none";
            // alerts[i].style.display = "none";
            // trends[i].style.display = "none";
        }
        else if (interval==="radar") {
            radar[i].style.display = "block";
            profileCard2.style.display = "block";
            today[i].style.display = "none";
            next48hours[i].style.display = "none";
            monthly[i].style.display = "none";
            alerts[i].style.display = "none";
            trends[i].style.display = "none";
            card2.style.display = "none";
            card3.style.display = "none";
            card4.style.display = "none";
            card5.style.display = "none";
            card6.style.display = "none";
            card7.style.display = "none";
            card8.style.display = "none";
        }
        else if (interval==="alerts") {
            alerts[i].style.display = "flex";
            profileCard2.style.display = "flex";
            radar[i].style.display = "none";
            monthly[i].style.display = "none";
            today[i].style.display = "none";
            next48hours[i].style.display = "none";
            trends[i].style.display = "none";
            card2.style.display = "none";
            card3.style.display = "none";
            card4.style.display = "none";
            card5.style.display = "none";
            card6.style.display = "none";
            card7.style.display = "none";
            card8.style.display = "none";
        }
        else if (interval==="trends") {
            trends[i].style.display = "flex";
            profileCard2.style.display = "flex";
            alerts[i].style.display = "none";
            radar[i].style.display = "none";
            monthly[i].style.display = "none";
            today[i].style.display = "none";
            next48hours[i].style.display = "none";
        }
        else {
            profileCard2.style.display = "flex";
            today[i].style.display = "none";
            next48hours[i].style.display = "none";
            monthly[i].style.display = "none";
            radar[i].style.display = "none";
            alerts[i].style.display = "none";
            trends[i].style.display = "none";
        }
    };
};