document.addEventListener("DOMContentLoaded", () => {
    const city = document.getElementById("city");
    for (let i = 0; i < 25; i++) {
        const building = document.createElement("div");
        const heightFactor = Math.random().toFixed(2); // entre 0.00 y 1.00
        building.className = "building";
        building.style.setProperty("--h", heightFactor);

        const windows = document.createElement("div");
        windows.className = "windows";

        for (let j = 0; j < 27; j++) {
            const windowDiv = document.createElement("div");
            windowDiv.className = "window";
            windows.appendChild(windowDiv);
        }

        building.appendChild(windows);
        city.appendChild(building);
    }
});