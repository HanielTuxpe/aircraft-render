const formulario = document.getElementById("formulario");
const resultado = document.getElementById("resultado");

formulario.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        engine_power: parseFloat(document.getElementById("engine_power").value),
        max_speed: parseFloat(document.getElementById("max_speed").value),
        cruise_speed: parseFloat(document.getElementById("cruise_speed").value),
        landing_distance: parseFloat(document.getElementById("landing_distance").value),
        empty_weight: parseFloat(document.getElementById("empty_weight").value),
        length: parseFloat(document.getElementById("length").value)
    };

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.error) {
            resultado.textContent = `Error: ${result.error}`;
            resultado.style.color = "red";
        } else {
            resultado.textContent = `Precio estimado: ${result.price}`;
            resultado.style.color = "green";
        }
    } catch (error) {
        resultado.textContent = "Error al procesar la solicitud.";
        resultado.style.color = "red";
    }
});
