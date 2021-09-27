window.addEventListener("DOMContentLoaded", (e) => {
    console.log("Main Script Loaded");

    // DOM Elements
    let profileButton = document.querySelector('.profile-button');
    

    let sidePanel = document.querySelector('.side-panel');




    // Event Listeners
    profileButton.addEventListener('click', e=>{
        e.preventDefault();

        sidePanel.classList.toggle('side-panel-hidden');
    })

    
});
