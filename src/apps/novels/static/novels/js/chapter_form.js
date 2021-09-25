let $chapterContent = document.querySelector('#chapter_content_input');
let $chapterForm = document.querySelector('#chapter_form');

$chapterForm.addEventListener('submit', e => {
    let chapterContent = quill.root.innerHTML;

    $chapterContent.value = chapterContent;

});