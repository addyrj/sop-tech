
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



function uploadImage(inputs) {

    let blocker = document.getElementById("blocker");
    if (!blocker) {
        blocker = document.createElement("div");
        blocker.id = "blocker";

        blocker.style.position = "fixed";
        blocker.style.top = "0";
        blocker.style.left = "0";
        blocker.style.width = "100%";
        blocker.style.height = "100%";
        blocker.style.background = "rgba(0,0,0,0.3)";
        blocker.style.zIndex = "9999";

        blocker.style.display = "flex";
        blocker.style.flexDirection = "column"; // 👈 important
        blocker.style.alignItems = "center";
        blocker.style.justifyContent = "center";
        blocker.style.color = "#fff";
        blocker.style.fontSize = "20px";
        blocker.style.fontWeight = "bold";

        document.body.appendChild(blocker);
    }

    blocker.style.display = "flex";
    blocker.innerHTML = "Please wait...<br><span id='progressText'>0%</span>";

    const fields = inputs.closest("tr");
    const files = fields.querySelector("input[type='file']").files;

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("images", files[i]);
    }

    const duration = fields.querySelector(".field-duration > input").value;
    const data = inputs.id.split("+");

    const tvlist = fields.querySelector(".field-display_tv").querySelectorAll("option");

    let tv = null;
    tvlist.forEach(function(result){
        if(result.selected){
            tv = result.innerText;
        }
    });

    formData.append("production_id", data[1]);
    formData.append("duration", duration);
    formData.append("tvname", tv);

    const xhr = new XMLHttpRequest();

    xhr.open("POST", "/sop/upload_image/", true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));

    // 📊 progress
    xhr.upload.onprogress = function (e) {
        if (e.lengthComputable) {
            let percent = Math.round((e.loaded / e.total) * 100);
            document.getElementById("progressText").innerText = percent + "%";
        }
    };

    xhr.onload = function () {
        if (xhr.status === 200) {
            alert("Upload successfully!");
        } else {
            alert("Upload failed!");
        }
        window.location.reload();
    };

    xhr.onerror = function () {
        alert("Upload failed!");
        window.location.reload();
    };

    xhr.send(formData);
}




(function() {
    function init() {
        if (typeof django === "undefined" || typeof django.jQuery === "undefined") {
            setTimeout(init, 50);
            return;
        }

        var $ = django.jQuery;

        $(document).ready(function() {







            

            $(document).on("click", ".select-files-btn", function () {

                const row = $(this).closest("tr");
                const displayTv = row.find('select[name$="display_tv"]').val();

                if (!displayTv) {
                    alert("Please select Display TV first");
                    return;
                }

                // Save reference to the active inline row (DOM element!)
                window._activeInlineRow = row[0];

                // Create modal if it doesn't exist
                if ($("#media-bucket-modal").length === 0) {
                    $("body").append(`
                        <div id="media-bucket-modal" style="display:none;">
                            <div class="mb-overlay"></div>
                            <div class="mb-modal">
                                <div class="mb-header">
                                    <span>Select Media Files</span>
                                    <button type="button" class="mb-close">×</button>
                                </div>
                                <iframe id="media-bucket-iframe" style="width:100%;height:100%;border:none;"></iframe>
                            </div>
                        </div>
                    `);
                }

                // Open modal
                $("#media-bucket-iframe").attr("src", `/admin/sop/productionline/mediabucket/select/`);
                $("#media-bucket-modal").fadeIn(200);

            });

            // Close modal
            $(document).on("click", ".mb-close, .mb-overlay", function () {
                $("#media-bucket-iframe").attr("src", "");
                $("#media-bucket-modal").fadeOut(200);
            });

            /* ==================================================
               FILE SIZE VALIDATION (ADDED BELOW – NO CHANGES ABOVE)
               ================================================== */

            const MAX_SIZE_MB = 400;
            const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;

            // Global flag to block admin submit
            window._fileSizeInvalid = false;

            // Validate file size on selection
            $(document).on("change", "input[type='file']", function () {

                const files = this.files;
                window._fileSizeInvalid = false;

                if (!files || !files.length) return;

                for (let i = 0; i < files.length; i++) {

                    if (files[i].size > MAX_SIZE_BYTES) {

                        alert(
                            `❌ File too large\n\n` +
                            `File: ${files[i].name}\n` + 
                            `Maximum allowed size: 400 MB`
                        );

                        // Clear input to prevent upload
                        this.value = "";

                        // Mark invalid
                        window._fileSizeInvalid = true;
                        return;
                    }
                }
            });

            // Block Django admin save button (prevents spinner)
            $("form").on("submit", function (e) {
                if (window._fileSizeInvalid) {
                    e.preventDefault();
                    e.stopImmediatePropagation();
                    alert("Please remove oversized files before saving.");
                    return false;
                }
            });

            /* ===========================
               END FILE SIZE VALIDATION
               =========================== */
               
            /* ==================================================
               UPLOAD BACKDROP + PROGRESS BAR (ADDED)
               ================================================== */

            function ensureUploadOverlay() {
                if ($("#upload-overlay").length) return;

                $("body").append(`
                    <div id="upload-overlay" style="
                        position: fixed;
                        inset: 0;
                        background: rgba(0,0,0,0.6);
                        z-index: 99999;
                        display: none;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    ">
                        <div style="
                            background: #fff;
                            padding: 30px;
                            width: 420px;
                            border-radius: 8px;
                            text-align: center;
                            box-shadow: 0 10px 40px rgba(0,0,0,.3);
                        ">
                            <h3>Uploading files…</h3>
                            <div style="width:100%;background:#e5e5e5;border-radius:6px;overflow:hidden;margin-top:15px;">
                                <div id="upload-progress-bar" style="
                                    width:0%;
                                    height:22px;
                                    background:#79aec8;
                                    transition:width 0.15s;
                                "></div>
                            </div>
                            <p id="upload-progress-text" style="margin-top:10px;">0%</p>
                        </div>
                    </div>
                `);
            }

            $(document).on("submit", "form", function (e) {

                if (window._fileSizeInvalid) {
                    return;
                }

                e.preventDefault();
                e.stopImmediatePropagation();

                ensureUploadOverlay();
                $("#upload-overlay").fadeIn(200);

                uploadFormWithProgress(this);
            });

            function uploadFormWithProgress(form) {
                const formData = new FormData(form);
                let isDelete = form.querySelectorAll("input[type='checkbox']")

                if (isDelete.length > 0 && isDelete[0].checked == true) {
                    document.querySelector("#upload-overlay h3").innerText = "Deleting files...";
                }

                const xhr = new XMLHttpRequest();

                xhr.open("POST", form.action, true);
                xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

                xhr.upload.onprogress = function (e) {
                    if (e.lengthComputable) {
                        const percent = Math.round((e.loaded / e.total) * 100);
                        $("#upload-progress-bar").css("width", percent + "%");
                        $("#upload-progress-text").text(percent + "%");
                    }
                };


                xhr.onload = function () {
                    if (xhr.status === 200) {
                        let redirectUrl = '/admin/sop/mediacontent/'; // fallback
                        // let message = "";

                        try {
                            const data = JSON.parse(xhr.responseText);
                            if (data.redirect_url) redirectUrl = data.redirect_url;
                            // if (data.message) message = data.message;
                        } catch (e) {
                            console.warn("Response not JSON, using fallback URL");
                        }

                        $("#upload-progress-bar").css("width", "100%");
                        $("#upload-progress-text").text("100%");



                        // Redirect after a short delay
                        setTimeout(function () {
                            $("#upload-overlay").fadeOut(200);
                            window.location.href = redirectUrl;
                        }, 1000);
                    } else {
                        alert("Upload failed. Please try again.");
                        $("#upload-overlay").fadeOut(200);
                    }
                };

                xhr.onerror = function () {
                    alert("Network error during upload.");
                    $("#upload-overlay").fadeOut(200);
                };

                xhr.send(formData);
            }

        });
    }

    init();
})();
