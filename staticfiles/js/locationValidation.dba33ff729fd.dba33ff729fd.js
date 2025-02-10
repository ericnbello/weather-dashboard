function getErrorInfo() {
    const location = document.getElementById("location");

    if (!location.checkValidity())
        document.getElementById("location-error").innerHTML = 'Location not found. Search must be in the form of "City", "City, State, Country" or "City, Country".';
    else 
        document.getElementById("location-error").innerHTML = "";
}

function validateForm() {
    document.addEventListener('invalid', (function () {
        return function (e) {
            e.preventDefault();
        };
    })(), true);

    document.querySelectorAll("#location-search input").forEach(function (element) {
        element.addEventListener('blur', function () {
            getErrorInfo();
        });
    });

    document.querySelectorAll("#location-search input").forEach(function (element) {
        element.addEventListener('blur', function () {
            // if input field passes validation remove the error class, else add it
            if (this.checkValidity()) {
                this.classList.remove('error-input');
            }
            else {
                this.classList.add('error-input');
            }
        });
    });

    /* submit event on form */
    document.querySelector("#location-search").addEventListener('submit', function (e) {
        // if form has not passed validation 
        if (!this.checkValidity()) {
            // check validation for each input field inside the form
            // if input field is valid then remove the error class, else add it
            this.querySelectorAll("input").forEach(function (element) {
                if (element.checkValidity())
                    element.classList.remove('error-input');
                else
                    element.classList.add('error-input');
            });
            getErrorInfo();
            e.preventDefault();
        }
        else {
            // document.getElementById("location-error").innerHTML = 'Location not found. Search must be in the form of "City", "City, State, Country" or "City, Country".';
            // e.preventDefault();
            // document.location.href="/";
        }
    });
}