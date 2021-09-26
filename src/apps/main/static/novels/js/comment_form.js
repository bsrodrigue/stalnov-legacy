let $commentContent = document.querySelector('#comment_input');
let $commentForm = document.querySelector('#comment_form');

$commentForm.addEventListener('submit', e => {
    let chapterContent = quill.root.innerHTML;
    console.log(chapterContent);
    $commentContent.value = chapterContent;
});