// function toggleInterval(interval) {
//     const daily = document.getElementsByClassName("daily");
//     const hourly = document.getElementsByClassName("hourly");

//     for (var i = 0; i < daily.length; i++) {
//         if(interval==="daily"){
//             daily[i].style.display = "flex";
//             hourly[i].style.display = "none";
//         }
//         else {
//             hourly[i].style.display = "flex";
//             daily[i].style.display = "none";
//         }
//     };
// };

function toggleInterval(interval) {

    // e.preventDefault();
    
    const daily = document.getElementsByClassName("daily");
    const weekly = document.getElementsByClassName("weekly");
    const monthly = document.getElementsByClassName("monthly");
    const radar = document.getElementsByClassName("radar");
    const card = document.getElementsByClassName("card");
    const timeCards = document.getElementById("time-cards");
    const alerts = document.getElementsByClassName("alerts");
    const blankMonthlyCard = document.getElementsByClassName("blank-monthly-card");
    // const blankMonthlyCardInfo = document.getElementsByClassName("blank-monthly-card-info");


    for (var i = 0; i < daily.length; i++) {
        if(interval==="daily"){
            daily[i].style.display = "flex";
            // daily[i].style.visibility = "visible";
            weekly[i].style.display = "none";
            monthly[i].style.display = "none";
            // blankMonthlyCard[i].style.display = "block";
            // blankMonthlyCard[i].style.visibility = "visible";

            // radar[i].style.display = "none";
            // alerts[i].style.display = "none";
            // timeCards.style.display = "flex";
            // card.style.display = "flex";
        }
        else if (interval==="weekly") {
            // blankMonthlyCard[i].style.visibility = "visible";
            weekly[i].style.display = "flex";
            // weekly[i].style.visibility = "visible";
            daily[i].style.display = "none";
            monthly[i].style.display = "none";
            // blankMonthlyCard[i].style.display = "block";
            // radar[i].style.display = "none";
            // alerts[i].style.display = "none";
            // timeCards.style.display = "flex";
            // card.style.display = "flex";
        }
        else if (interval==="monthly") {
            monthly[i].style.display = "flex";
            // blankMonthlyCard[i].style.display = "none";
            // blankMonthlyCard[i].style.visibility = "hidden";

            // blankMonthlyCardInfo[i].style.color = "hsl(246, 80%, 60%)";
            // monthly[i].style.visibility = "visible";
            daily[i].style.display = "none";
            weekly[i].style.display = "none";
            // radar[i].style.display = "none";
            // alerts[i].style.display = "none";
            // timeCards.style.display = "flex";
            // card.style.display = "flex";
        }
        // else if (interval==="radar") {
        //     radar[i].style.display = "flex";
        //     radar[i].style.visibility = "visible";
        //     monthly[i].style.display = "none";
        //     daily[i].style.display = "none";
        //     weekly[i].style.display = "none";
        //     timeCards.style.display = "none";
        //     card.style.display = "none";
        //     alerts[i].style.display = "none";
        //     alerts[i].style.visibility = "hidden";
        // }
        // else if (interval==="alerts") {
        //     alerts[i].style.display = "flex";
        //     alerts[i].style.visibility = "visible";
        //     radar[i].style.display = "none";
        //     radar[i].style.visibility = "hidden";
        //     monthly[i].style.display = "none";
        //     daily[i].style.display = "none";
        //     weekly[i].style.display = "none";
        //     timeCards.style.display = "none";
        //     card.style.display = "none";
        // }
        else {
            daily[i].style.display = "none";
            weekly[i].style.display = "none";
            monthly[i].style.display = "none";
            // blankMonthlyCard[i].style.display = "none";
            // radar[i].style.display = "none";
            // radar[i].style.visibility = "visible";
            // alerts[i].style.display = "none";
            // alerts[i].style.visibility = "visible";
            // timeCards.style.display = "flex";
            // card.style.display = "flex";
        }
    };
};