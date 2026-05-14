








(function () {
    if (!window.django || !django.jQuery) {
        console.error("django.jQuery not available");
        return;
    }




    const $ = django.jQuery;

    // ✅ Centralized window cleanup
    function clearWindowState() {
        delete window._activeMediaFileForm;
        delete window._activeSelectButton;
        console.log("✅ Window state cleared");
    }



    // ✅ CSRF helper
    function getCSRFToken() {
        const el = document.querySelector('[name=csrfmiddlewaretoken]');
        return el ? el.value : "";
    }

    $(document).ready(function () {
        console.log("django.jQuery ready");


        /* ==================================================
           FILE SIZE VALIDATION (ADDED — FRONTEND ONLY)
           ================================================== */

        const MAX_SIZE_MB = 400;
        const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;

        // Global flag to stop submit
        window._mediaFileSizeInvalid = false;

        // Validate file when chosen
        $(document).on("change", "input[type='file']", function () {

            const files = this.files;
            window._mediaFileSizeInvalid = false;

            if (!files || !files.length) return;

            for (let i = 0; i < files.length; i++) {
                if (files[i].size > MAX_SIZE_BYTES) {

                    alert(
                        `❌ File too large\n\n` +
                        `File: ${files[i].name}\n` + 
                        `Maximum allowed size: ${MAX_SIZE_MB} MB`
                    );

                    // Clear input to stop upload
                    this.value = "";

                    window._mediaFileSizeInvalid = true;
                    return;
                }
            }
        });

        // Block submit (prevents spinner)
        $(document).on("submit", "form", function (e) {
            if (window._mediaFileSizeInvalid) {
                e.preventDefault();
                e.stopImmediatePropagation();
                alert("Please remove oversized files before submitting.");
                return false;
            }
        });

        /* =======================
           END FILE SIZE VALIDATION
           ======================= */

        // Open modal
        $(document).on("click", ".select-files-btn", function () {
            console.log("Select Files button clicked");

            window._activeMediaFileForm = $(this).closest("form")[0];
            window._activeSelectButton = this;

            if ($("#mediafile-modal").length === 0) {
                $("body").append(`
                    <div id="mediafile-modal"
                         style="position:fixed; inset:0; background:rgba(0,0,0,.6); z-index:9999;">
                        <div style="width:80%; height:80%; background:#fff; margin:5% auto;
                                    padding:10px; position:relative; border-radius:6px;">
                            
                            <button id="terminate-modal-btn"
                                    style="position:absolute; top:8px; right:12px;
                                           font-size:26px; background:none; border:none; cursor:pointer;">
                                ×
                            </button>

                            <iframe id="mediafile-iframe"
                                    src="/sop/mediabucket/select/"
                                    style="width:100%; height:100%; border:none;">
                            </iframe>
                        </div>
                    </div>
                `);
            }
            // ✅ ALWAYS reload iframe when opening
            $("#mediafile-iframe").attr("src", "/sop/mediabucket/select/");
            $("#mediafile-modal").show();
        });

        // ❌ Close modal
        $(document).on("click", "#terminate-modal-btn", function () {
            $("#mediafile-modal").hide();
            $("#mediafile-iframe").attr("src", "");
            clearWindowState();
        });

        // ✅ Called by iframe
        window.setSelectedMediaFiles = function (fileIds) {
            if (!Array.isArray(fileIds)) {
                console.error("Invalid fileIds:", fileIds);
                return;
            }

            if (!window._activeMediaFileForm || !window._activeSelectButton) {
                console.error("Active form/button missing");
                return;
            }

            const $form = $(window._activeMediaFileForm);
            const $hiddenInput = $form.find('input[name="selected_files_ids"]');

            if ($hiddenInput.length === 0) {
                console.error("Hidden field selected_files_ids missing");
                return;
            }

            // Store IDs
            $hiddenInput.val(fileIds.join(","));
            console.log("Stored IDs:", $hiddenInput.val());

            // Update button label
            $(window._activeSelectButton)
                .text(`${fileIds.length} files selected`);

            // Close modal
            $("#mediafile-modal").hide();
            $("#mediafile-iframe").attr("src", "");

            // ✅ Clear window state LAST
            clearWindowState();
        };



        /* ==================================================
           BACKDROP + PROGRESS BAR (WORKING)
           ================================================== */

        const $form = $(".custom-form-container form");
        if (!$form.length) return;

        function ensureBackdrop() {
            if ($("#mediafile-backdrop").length) return;

            $("body").append(`
                <div id="mediafile-backdrop" style="
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
                        padding:30px;
                        width:420px;
                        border-radius:8px;
                        text-align:center;
                    ">
                        <h3>Updating media file…</h3>
                        <div style="margin-top:18px;">
                            <div style="height:10px;background:#e5e5e5;border-radius:6px;">
                                <div id="mediafile-progress-bar"
                                     style="width:0%;height:10px;background:#4a90e2;border-radius:6px;">
                                </div>
                            </div>
                            <div id="mediafile-progress-text" style="margin-top:8px;">0%</div>
                        </div>
                    </div>
                </div>
            `);
        }

        // ✅ Namespaced submit handler (IMPORTANT)
        $form.on("submit.mediaBackdrop", function (e) {
            if (window._mediaFileSizeInvalid) return;

            e.preventDefault();
            ensureBackdrop();
            $("#mediafile-backdrop").fadeIn(200);

            submitWithProgress(this);
        });

        function submitWithProgress(form) {
            const formData = new FormData(form);
            const xhr = new XMLHttpRequest();

            xhr.open("POST", window.location.href, true);
            xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());

            xhr.upload.onprogress = function (e) {
                if (!e.lengthComputable) return;
                const percent = Math.round((e.loaded / e.total) * 100);
                $("#mediafile-progress-bar").css("width", percent + "%");
                $("#mediafile-progress-text").text(percent + "%");
            };

            xhr.onload = function () {
                if (xhr.status === 200) {
                    $("#mediafile-progress-bar").css("width", "100%");
                    $("#mediafile-progress-text").text("100%");

                    let redirectUrl = "";
                    try {
                        const data = JSON.parse(xhr.responseText);
                        redirectUrl = data.redirect_url || "";
                    } catch (e) {}

                    setTimeout(function () {
                        $("#mediafile-backdrop").fadeOut(200);
                        if (redirectUrl) window.location.href = redirectUrl;
                    }, 600);
                } else {
                    alert("Save failed. Please try again.");
                    $("#mediafile-backdrop").fadeOut(200);
                }
            };

            xhr.onerror = function () {
                alert("Network error during save.");
                $("#mediafile-backdrop").fadeOut(200);
            };

            xhr.send(formData);
        }
    });
})();



/* ==========================================================
   BACKDROP + PROGRESS BAR (APPENDED – NO EXISTING CODE TOUCHED)
   ========================================================== */

(function () {

    if (!window.django || !django.jQuery) return;
    const $ = django.jQuery;

    $(document).ready(function () {

        /* Apply ONLY on MediaFile update page */
        const $form = $(".custom-form-container form");
        if (!$form.length) return;

        /* ---------- Create backdrop once ---------- */
        function ensureBackdrop() {
            if ($("#mediafile-backdrop").length) return;

            $("body").append(`
                <div id="mediafile-backdrop" style="
                    position:fixed;
                    inset:0;
                    background:rgba(0,0,0,0.65);
                    z-index:10050;
                    display:none;
                    align-items:center;
                    justify-content:center;
                ">
                    <div style="
                        background:#fff;
                        padding:28px;
                        width:420px;
                        border-radius:10px;
                        text-align:center;
                    ">
                        <h3>Saving media file…</h3>

                        <div style="margin-top:18px;">
                            <div style="height:10px;background:#e5e5e5;border-radius:6px;">
                                <div id="mediafile-progress-bar"
                                     style="width:0%;height:10px;background:#4a90e2;border-radius:6px;">
                                </div>
                            </div>
                            <div id="mediafile-progress-text" style="margin-top:8px;">0%</div>
                        </div>
                    </div>
                </div>
            `);
        }

        /* ---------- Intercept submit ---------- */
        $form.on("submit", function (e) {

            // respect existing file validation
            if (window._mediaFileSizeInvalid) return;

            e.preventDefault();
            e.stopImmediatePropagation();

            ensureBackdrop();
            $("#mediafile-backdrop").fadeIn(200);

            submitWithProgress(this);
        });

        /* ---------- AJAX submit with progress ---------- */
        function submitWithProgress(form) {

            const formData = new FormData(form);
            const xhr = new XMLHttpRequest();

            xhr.open("POST", window.location.href, true);
            xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

            xhr.upload.onprogress = function (e) {
                if (!e.lengthComputable) return;

                const percent = Math.round((e.loaded / e.total) * 100);
                $("#mediafile-progress-bar").css("width", percent + "%");
                $("#mediafile-progress-text").text(percent + "%");
            };

            xhr.onload = function () {
                if (xhr.status === 200) {

                    $("#mediafile-progress-bar").css("width", "100%");
                    $("#mediafile-progress-text").text("100%");

                    let redirectUrl = "";
                    try {
                        const data = JSON.parse(xhr.responseText);
                        redirectUrl = data.redirect_url || "";
                    } catch (err) {}

                    setTimeout(function () {
                        $("#mediafile-backdrop").fadeOut(200);
                        if (redirectUrl) {
                            window.location.href = redirectUrl;
                        }
                    }, 600);

                } else {
                    alert("Save failed. Please try again.");
                    $("#mediafile-backdrop").fadeOut(200);
                }
            };

            xhr.onerror = function () {
                alert("Network error during save.");
                $("#mediafile-backdrop").fadeOut(200);
            };

            xhr.send(formData);
        }

    });

})();

