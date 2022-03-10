let $previousButtons = document.querySelectorAll(".signup-form-previous");
let $nextButtons = document.querySelectorAll(".signup-form-next");
let $formSteps = document.querySelectorAll(".signup-form-step");
let $signupForm = document.querySelector("#signup-form");

const LAST_STEP = 3;
const FIRST_STEP = 1;

$previousButtons.forEach(($button) => {
    $button.addEventListener("click", (e) => {
        e.preventDefault();
        const STEP = parseInt($button.getAttribute("data-step"));

        if (STEP === FIRST_STEP) {
            return;
        }
        // Hide all steps
        $formSteps.forEach(($formStep) => {
            $formStep.hidden = true;
        });

        // Show previous step
        let $previousFormStep = document.querySelector(
            `.signup-form-step-${STEP - 1}`
        );
        $previousFormStep.hidden = false;
    });
});

$nextButtons.forEach(($button) => {
    $button.addEventListener("click", (e) => {
        e.preventDefault();
        const STEP = parseInt($button.getAttribute("data-step"));

        if (STEP === LAST_STEP) {
            $signupForm.submit();
        }
        // Hide all steps
        $formSteps.forEach(($formStep) => {
            $formStep.hidden = true;
        });

        // Show next step
        let $nextFormStep = document.querySelector(
            `.signup-form-step-${STEP + 1}`
        );
        $nextFormStep.hidden = false;
    });
});
