window.addEventListener("DOMContentLoaded", (e) => {
    let profileButton = document.querySelector(".profile-button");
    let sidePanel = document.querySelector(".side-panel");
    let genderInputs = document.querySelectorAll(".gender-input");
    let modalContainer = document.querySelector(".modal-container");

    // Reorder Chapters
    let chapterList = document.querySelector("#dashboard-chapter-list");
    const SORTABLE_OPTIONS = {
        animation: 150,
        onChange: function (e) {
            console.log(e);
        },
    };

    try {
        let sortable = Sortable.create(chapterList, SORTABLE_OPTIONS);
    } catch (e) {
        console.error("Sortable does not seem to work here...");
    }

    // Toggle Side-Panel
    profileButton.addEventListener("click", (e) => {
        e.preventDefault();
        sidePanel.classList.toggle("side-panel-hidden");
    });

    // Signup Form
    genderInputs.forEach((input) => {
        function clearGenderRadios() {
            let genderRadios = document.querySelectorAll(".gender-radio");
            let genderIcons = document.querySelectorAll(".gender-icon");

            genderRadios.forEach((radio) => {
                radio.checked = false;
            });

            genderIcons.forEach((icon) => {
                icon.classList.remove("gender-is-selected");
            });
        }
        input.addEventListener("click", (e) => {
            e.preventDefault();
            let gender = e.target.getAttribute("data-gender");
            if (gender) {
                switch (gender) {
                    case "H":
                        clearGenderRadios();
                        document.getElementById("gender-male").checked = true;
                        document
                            .querySelector(".fa-male")
                            .classList.add("gender-is-selected");
                        break;

                    case "F":
                        clearGenderRadios();
                        document.getElementById("gender-female").checked = true;
                        document
                            .querySelector(".fa-female")
                            .classList.add("gender-is-selected");
                        break;

                    default:
                        break;
                }
            }
        });
    });

    // Modals
    document.querySelectorAll(".novel-item-action-delete").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            console.log("Delete");
            modalContainer.classList.add("modal-container-show");
            document
                .querySelector(".btn-cancel")
                .addEventListener("click", (e) => {
                    e.preventDefault();
                    modalContainer.classList.remove("modal-container-show");
                });
            document
                .querySelector(".btn-confirm")
                .addEventListener("click", (e) => {
                    const submitLink = btn.getAttribute("data-url");
                    if (submitLink) {
                        document.querySelector(".btn-confirm").href =
                            submitLink;
                        document.querySelector(".btn-confirm").click();
                    }
                });
        });
    });
});
