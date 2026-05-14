



function openPublishModal() {

    const modalHTML = `
    <div class="modal fade" id="publishModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">

          <div class="modal-header">
            <h5 class="modal-title">Publishing</h5>
          </div>

          <div class="modal-body">
            <div class="progress mb-2">
              <div id="publishProgress"
                   class="progress-bar progress-bar-striped progress-bar-animated"
                   style="width:0%">0%</div>
            </div>
            <div id="publishStatus">Waiting for TVs...</div>
          </div>

        </div>
      </div>
    </div>
    `;

    document.body.insertAdjacentHTML("beforeend", modalHTML);

    const modalEl = document.getElementById("publishModal");

    const modal = new bootstrap.Modal(modalEl, {
        backdrop: 'static',   // outside click disable
        keyboard: false       // ESC disable
    });

    modal.show();
}





function deletedata(e){
    const csrf = getCookie("csrftoken")
    console.log(csrf)
    fetch("/sop/delete_content/",{
            method:"POST",
            credentials: "same-origin",
            headers:{"Content-Type":"application/json","X-CSRFToken":csrf},
            body:JSON.stringify({"production_id":parseInt(e.id.split("+")[0]),"bucket_id":parseInt(e.id.split("+")[1]),"duration":parseInt(e.id.split("+")[2]),"media_system_id":parseInt(e.id.split("+")[3])})
        }).then(response=>{
            return response.json()        
    }).then(result=>{
        alert("Unpublished")
        window.location.reload()
    })}



function publish(e) {
    openPublishModal();

    const csrf = getCookie("csrftoken");

    const [production_id, bucket_id, duration, media_system_id] =
        e.id.split("+").map(Number);

    fetch("/sop/publish/", {
        method: "POST",
        credentials: "same-origin",
        headers: {"Content-Type": "application/json","X-CSRFToken": csrf},
        body: JSON.stringify({ production_id, bucket_id, duration, media_system_id })
    });

    const progressBar = document.getElementById("publishProgress");
    const statusDiv = document.getElementById("publishStatus");
    progressBar.style.width = 100 + "%";
    progressBar.innerText = 100 + "%";
    setTimeout(()=>{
        window.location.reload()
    },2000)

    let lastCompletedCount = 0;

    const interval = setInterval(() => {

        fetch(`/sop/tv-download-status/${production_id}/`)
        .then(res => res.json())
        .then(data => {

            const percent = Math.floor((data.completed / data.total) * 100);

            progressBar.style.width = percent + "%";
            progressBar.innerText = percent + "%";

            // agar naya TV complete hua
            if(data.completed > lastCompletedCount){

                const completedTV = data.tvs.find(tv => tv.status === "completed" && !tv.shown);

                if(completedTV){
                    statusDiv.innerHTML =
                        `📺 ${completedTV.tv_name} Download Completed`;
                }

                lastCompletedCount = data.completed;
            }

            if (data.completed === data.total) {

                clearInterval(interval);

                statusDiv.innerHTML += "<br>✅ All TVs completed";

                setTimeout(()=>{
                    window.location.reload();
                },1500);
            }

        });

    },3000);
}



// loggintv()
function toggleDeleteButton() {

    // All checkboxes
    let checkboxes =document.querySelectorAll(".mediafile-checkbox");

    // Checked checkboxes
    let checked =document.querySelectorAll(".mediafile-checkbox:checked");

    let deleteBtn = document.getElementById("handlebtn");


}

const x = document.querySelector(".mediafile-checkbox")
// Run on checkbox click
document.addEventListener("change", function(e) {
    if (e.target.classList.contains("mediafile-checkbox")) {
        toggleDeleteButton();
    }

});









function deletetest() {
    // Get all checked checkboxes
    let selected = document.querySelectorAll('.mediafile-checkbox:checked');
    let ids = [];

    selected.forEach((x)=>{
        ids.push(x.value);
    });

//     // Send to Django
    fetch("/sop/user/api/deletemultple/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")            
        },
        body: "ids=" + ids.join(",")
    })
    .then(res => res.json())
    .then(data => {
        setTimeout(()=>{
            if (data.success) {
                    window.location.reload()
            }else{
                alert("Failed")
            }
        },500)

    });
}


// CSRF helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        document.cookie.split(";").forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}






window.addEventListener("load", () => {

    const production = document.getElementById("id_production_line");
    const folder = document.getElementById("id_select_folder");

    if (!production || !folder) return;

    // 🔥 CREATE FETCH BUTTON
    const fetchBtn = document.createElement("button");
    fetchBtn.type = "button";
    fetchBtn.textContent = "Get TV";
    fetchBtn.setAttribute("onclick","test()")
    fetchBtn.style.cssText = `
        margin-top:10px;
        padding:6px 12px;
        background:#0d6efd;
        color:white;
        border:none;
        border-radius:6px;
        cursor:pointer;
    `;

    folder.parentElement.appendChild(fetchBtn);
})















function test(){

    const production = document.getElementById("id_production_line");
    const folder = document.getElementById("id_select_folder");

    // Track last values to prevent duplicate triggers
    let lastProduction = production.value;
    let lastFolder = folder.value;

        const prodVal = production.value;
        const folderVal = folder.value;







                const bucket_name =  folder.options[folder.selectedIndex].text

                const u = document.createElement("ul")

                fetch(`/admin/sop/mediasystem/get-images/?bucket_name=${bucket_name}&production_line_id=${prodVal}`).then(test=>{
                    try{
                        document.querySelector(".images-list").remove()
                    }catch(e){}

                    u.setAttribute("class","images-list")
                    u.style.cssText=`    
                                        padding:0;
                                        display:flex;
                                        list-style:none;
                                    border-radius:10px;
                                        overflow:hidden;`

                    
                    document.getElementById("content-main").appendChild(u)

                    return test.json()
                }).then(response=>{
                response.map(result => {
                    const li = document.createElement("li");
                    li.style.cssText = `
                        display:flex;
                        flex-direction: column;
                        gap:10px;
                        padding:15px;
                        border:3px solid black;
                        border-radius:12px;
                        width:250px;
                        transition:0.3s;
                    `;
                    li.onmouseover = () => li.style.transform = "scale(1.02)";
                    li.onmouseout = () => li.style.transform = "scale(1)";

                    // Title (TV Name)
                    const titleDiv = document.createElement("div");
                    titleDiv.innerHTML = `<strong>Name:</strong>`;

                    // Editable span
                    const editableSpan = document.createElement("span");
                    editableSpan.setAttribute("contentEditable", "true");
                    editableSpan.textContent = result.name || "N/A";
                    editableSpan.style.borderBottom = "1px dashed #ccc";
                    editableSpan.style.padding = "2px 4px";
                    editableSpan.style.marginLeft = "5px";

                    // Save Button
                    const saveBtn = document.createElement("button");
                    saveBtn.textContent = "Save";
                    saveBtn.style.display = "none";
                    saveBtn.style.marginTop = "5px";

                    // Show save button on edit
                    editableSpan.addEventListener("input", () => {
                        saveBtn.style.display = "inline-block";
                    });

                    // Save button click → direct backend update
                    saveBtn.addEventListener("click", () => {
                        const newValue = editableSpan.textContent.trim();

                        // Example Django URL endpoint
                        fetch(`/sop/update-name/`, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRFToken": getCookie("csrftoken") // CSRF token for Django
                            },
                            body: JSON.stringify({
                                id: result.id,        // Image/TV ID
                                name: newValue        // New name
                            })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.success) {
                                console.log("Updated successfully ✅", newValue);
                                saveBtn.style.display = "none"; // hide button
                            } else {
                                console.error("Update failed ❌", data.error);
                            }
                        })
                        .catch(err => console.error("Error:", err));
                    });

                    // Append editable span and button to title
                    titleDiv.appendChild(editableSpan);
                    titleDiv.appendChild(saveBtn);

                    // Image display
                    const imageDiv = document.createElement("div");
                    imageDiv.innerHTML = `<strong>Image:</strong> ${result.image || "N/A"}`;

                    // Append all to li
                    li.appendChild(titleDiv);
                    li.appendChild(imageDiv);

                    u.appendChild(li);
                });


                })

                
            




            // Yaha apna kaam karo (AJAX / fetch etc.)
        
    

}