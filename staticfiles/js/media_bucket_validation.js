(function () {

    function init() {
        if (typeof django === "undefined" || typeof django.jQuery === "undefined") {
            setTimeout(init, 50);
            return;
        }

        var $ = django.jQuery;

        $(document).ready(function () {

            /* ==================================================
               FILE SIZE VALIDATION
               ================================================== */

            const MAX_SIZE_MB = 400;
            const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;

            window._fileSizeInvalid = false;

            $(document).on("change", "input[type='file']", function () {

                const files = this.files;
                window._fileSizeInvalid = false;

                if (!files || !files.length) return;

                for (let i = 0; i < files.length; i++) {
                    if (files[i].size > MAX_SIZE_BYTES) {

                        alert(
                            `❌ File too large\n\n` +
                            `File: ${files[i].name}\n` +
                            `Maximum allowed size: ${MAX_SIZE_MB} MB`
                        );

                        this.value = "";
                        window._fileSizeInvalid = true;
                        return;
                    }
                }
            });

            /* ==================================================
               BACKDROP + PROGRESS BAR
               ================================================== */

            function ensureBackdrop() {
                if ($("#media-bucket-backdrop").length) return;

                $("body").append(`
                    <div id="media-bucket-backdrop" style="
                        position:fixed;
                        inset:0;
                        background:rgba(0,0,0,0.6);
                        z-index: 99999;
                        display:none;
                        display: flex;
                        align-items:center;
                        justify-content:center;
                    ">
                        <div style="
                            background:#fff;
                            padding:28px;
                            width:420px;
                            border-radius:10px;
                            text-align:center;
                            box-shadow:0 10px 40px rgba(0,0,0,.35);
                        ">
                            <h3>Uploading media file…</h3>

                            <div style="margin-top:18px;">
                                <div style="height:10px;background:#e5e5e5;border-radius:6px;">
                                    <div id="media-bucket-progress-bar"
                                         style="width:0%;height:10px;background:#4a90e2;border-radius:6px;">
                                    </div>
                                </div>
                                <div id="media-bucket-progress-text" style="margin-top:8px;">0%</div>
                            </div>
                        </div>
                    </div>
                `);
            }

            /* ==================================================
               INTERCEPT ADMIN SAVE
               ================================================== */

            $("form").on("submit.mediaBucket", function (e) {

                if (window._fileSizeInvalid) {
                    e.preventDefault();
                    e.stopImmediatePropagation();
                    alert("Please remove oversized files before saving.");
                    return false;
                }

                e.preventDefault();
                e.stopImmediatePropagation();

                ensureBackdrop();
                $("#media-bucket-backdrop").fadeIn(200);

                submitWithProgress(this);
            });

            /* ==================================================
               AJAX SUBMIT WITH PROGRESS
               ================================================== */

            function submitWithProgress(form) {

                const formData = new FormData(form);
                const xhr = new XMLHttpRequest();

                xhr.open("POST", window.location.href, true);
                xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

                xhr.upload.onprogress = function (e) {
                    if (!e.lengthComputable) return;

                    const percent = Math.round((e.loaded / e.total) * 100);
                    $("#media-bucket-progress-bar").css("width", percent + "%");
                    $("#media-bucket-progress-text").text(percent + "%");
                };

                xhr.onload = function () {
                    if (xhr.status === 200) {

                        $("#media-bucket-progress-bar").css("width", "100%");
                        $("#media-bucket-progress-text").text("100%");

                        let redirectUrl = "";
                        try {
                            const data = JSON.parse(xhr.responseText);
                            redirectUrl = data.redirect_url || "";
                        } catch (e) {}

                        setTimeout(function () {
                            $("#media-bucket-backdrop").fadeOut(200);
                            if (redirectUrl) window.location.href = redirectUrl;
                        }, 600);

                    } else {
                        alert("Save failed. Please try again.");
                        $("#media-bucket-backdrop").fadeOut(200);
                    }
                };

                xhr.onerror = function () {
                    alert("Network error during upload.");
                    $("#media-bucket-backdrop").fadeOut(200);
                };

                xhr.send(formData);
            }

        });
    }

    init();

})();
