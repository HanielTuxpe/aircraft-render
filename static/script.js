document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("formulario");
    const resultado = document.getElementById("resultado");

    formulario.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(formulario);

        try {
            const response = await fetch("/predict", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();

            if (data.error) {
                resultado.textContent = `Error: ${data.error}`;
                resultado.style.color = "red";
            } else {
                resultado.textContent = `Precio estimado: ${data.price}`;
                resultado.style.color = "green";
            }
        } catch (error) {
            resultado.textContent = "Error al procesar la solicitud.";
            resultado.style.color = "red";
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const plane = document.getElementById("plane");

    // Animar el avión cada 5 segundos
    setInterval(() => {
        plane.style.transition = "none";
        plane.style.right = "-450px";

        setTimeout(() => {
            plane.style.transition = "right 4s linear";
            plane.style.right = "110%";
        }, 100);
    }, 5000);
});
