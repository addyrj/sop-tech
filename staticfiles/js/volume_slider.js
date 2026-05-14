document.addEventListener("DOMContentLoaded", function () {
    const sliders = document.querySelectorAll(".volume-slider");

    sliders.forEach(slider => {
        // Create value label
        const valueLabel = document.createElement("span");
        valueLabel.style.marginLeft = "10px";
        valueLabel.style.fontWeight = "bold";
        valueLabel.innerText = slider.value;

        slider.after(valueLabel);

        // Update label on slide
        slider.addEventListener("input", function () {
            valueLabel.innerText = this.value;
        });
    });
});
