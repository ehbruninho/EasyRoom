document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("plan_id").addEventListener("change", function () {
        const selectedOption = this.options[this.selectedIndex];
        const duration = parseInt(selectedOption.getAttribute("data-duration"));
        const dateInitInput = document.getElementById("date_init");
        const dateEndInput = document.getElementById("date_end");

        if (dateInitInput.value && !isNaN(duration)) {
            let startDate = new Date(dateInitInput.value);
            startDate.setHours(startDate.getHours() + duration);

            let year = startDate.getFullYear();
            let month = String(startDate.getMonth() + 1).padStart(2, "0");
            let day = String(startDate.getDate()).padStart(2, "0");
            let hours = String(startDate.getHours()).padStart(2, "0");
            let minutes = String(startDate.getMinutes()).padStart(2, "0");

            let formattedDate = `${year}-${month}-${day}T${hours}:${minutes}`;
            dateEndInput.value = formattedDate;
        }
    });

    document.getElementById("date_init").addEventListener("change", function () {
        document.getElementById("plan_id").dispatchEvent(new Event("change"));
    });
});
