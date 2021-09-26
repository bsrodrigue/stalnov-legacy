let $chapterList = $('.novel-chapter-list');
let $chapterListToggle = $('.chapter-list-toggle');

$chapterListToggle.click(()=>{
    console.log($chapterList.css('display'));
    $chapterList.toggle(400);
});