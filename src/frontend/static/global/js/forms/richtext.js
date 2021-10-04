window.addEventListener("DOMContentLoaded", (e) => {
    let $input = document.querySelector("#richtext_input");

    if(!$input){
        console.error('Input field not found');
        return;
    }

    if (!quill) {
        console.error("Quill is not imported, cannot save text.");
        return;
    }

    quill.on("text-change", function (delta, oldDelta, source) {
        let quillText = quill.root.innerHTML;
        $input.value = quillText;
    });
});
