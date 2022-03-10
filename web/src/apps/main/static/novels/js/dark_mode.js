$('#dark-mode-toggle-button').click(()=>{
    $('body').toggleClass('dark-mode-body');
    $('h1, h2, h3, h4, h5, h6, small, svg, a, p').toggleClass('dark-mode-text');
});