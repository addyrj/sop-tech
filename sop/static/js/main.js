
document.addEventListener("DOMContentLoaded", function () {
    let allorderfields = document.querySelectorAll(".order_select");
    allorderfields.forEach((myfield)=>{
        myfield.addEventListener("change", (e)=>{
            e.preventDefault();
            my_value = e.target.value;
            my_id = e.target.id;

            console.log(my_value, my_id);



            fetch("/sop/update-order/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: `id=${my_id}&value=${my_value}`
            })
            .then(res => res.json())
            .then(data => console.log("Response:", data));           
        })
    })
});



// CSRF token extractor
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}