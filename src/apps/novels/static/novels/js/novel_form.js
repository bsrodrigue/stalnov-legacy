const $form = document.querySelector("#novel_form");
const $novelDescription = document.querySelector("#novel_description_input");
const $defaultCovers = document.querySelectorAll(".default-cover");
const $customCoverUploadButton = document.querySelector(".upload-your-cover");
const $hiddenFileForm = document.getElementById("novel-form-cover-input");

function updateCoverUploadMessage(message) {
    document.querySelector(".upload-your-cover-subtext").innerHTML = message;
}

// TODO: Make sure that the novel content is really set before submitting
$form.addEventListener("submit", (e) => {
    let novelDescription = quill.root.innerHTML;
    $novelDescription.value = novelDescription;
});

// Handle default cover selection
$defaultCovers.forEach(($defaultCover) => {
    $defaultCover.addEventListener("click", (e) => {
        const selectedDefaultCoverIndex = e.target.getAttribute("data-index");

        // Select hidden radio button accordingly
        const $defaultCoverRadio = document.querySelector(
            `#default-cover-radio${selectedDefaultCoverIndex}`
        );
        $defaultCoverRadio.checked = true;

        // Visual update
        $defaultCovers.forEach(($defaultCover) => {
            $defaultCover.classList.remove("default-cover-selected");
        });
        e.target.classList.add("default-cover-selected");

        updateCoverUploadMessage("Vous avez choisi une couverture par defaut.");
    });
});

function deselectAllDefaultCovers() {
    $defaultCovers.forEach(($defaultCover) => {
        // Deselect hidden radio button accordingly
        const selectedDefaultCoverIndex =
            $defaultCover.getAttribute("data-index");
        const $defaultCoverRadio = document.querySelector(
            `#default-cover-radio${selectedDefaultCoverIndex}`
        );
        $defaultCoverRadio.checked = false;

        // Visual update
        $defaultCover.classList.remove("default-cover-selected");
    });
}

// Handle custom cover upload
$customCoverUploadButton.addEventListener("click", (e) => {
    e.preventDefault();
    console.log("Ready to upload your own cover.");
    $hiddenFileForm.click();
});

$hiddenFileForm.addEventListener("change", (e) => {
    let reader = new FileReader();
    reader.onloadend = () => {
        $customCoverUploadButton.style.backgroundImage = `url(${reader.result})`;
        $customCoverUploadButton.classList.add("cover-uploaded");
        document.querySelector(".fa-file-upload").style.color = "white";
        deselectAllDefaultCovers();
        updateCoverUploadMessage("Vous avez charge votre propre couverture.");
    };
    reader.readAsDataURL($hiddenFileForm.files[0]);
});
