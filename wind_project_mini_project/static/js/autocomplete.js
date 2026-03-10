document.addEventListener("DOMContentLoaded", () => {
    fetch("/static/data/countries.json")
        .then(response => response.json())
        .then(data => {
            const datalist = document.getElementById("countries");
            data.forEach(country => {
                const option = document.createElement("option");
                option.value = country;
                datalist.appendChild(option);
            });
        })
        .catch(error => console.error("Error loading country list:", error));
});
