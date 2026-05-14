// document.addEventListener("DOMContentLoaded", function () {
//     const toggleButton = document.getElementById("custom-action-btn");
//     if (!toggleButton) return;

//     toggleButton.addEventListener("click", function () {

//         console.log("hurrayyyy")
//         // Match all inline extra_data fields

//         const extraFields = document.querySelectorAll('input[name$="extra_data"]');

//         console.log(extraFields, "my extra field")
//         extraFields.forEach(field => {
//             field.style.display = field.style.display === "none" ? "block" : "none";
//         });
//     });
// });


document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("custom-action-btn");
    if (!toggleButton) return;

    toggleButton.addEventListener("click", function () {

        console.log("hurrayyyy");



        // Set hidden field: this tells Django validation that custom action is active
        const hiddenFlag = document.getElementById("custom_action");
        if (hiddenFlag) {
            hiddenFlag.value = "true";
            console.log("custom_action flag set to TRUE");
        }

        // Match all inline extra_data fields
        const extraFields = document.querySelectorAll('.sequence_order_field');

        console.log(extraFields)
        extraFields.forEach(field => {
            if (!field.id.includes("__prefix__")) {
                field.style.display = field.style.display === "none" ? "block" : "none";
            }
        });

    });
});
