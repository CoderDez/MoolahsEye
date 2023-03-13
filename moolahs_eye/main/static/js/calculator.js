
function submitFrequencyForm() {
    const select = document.getElementById("frequency_select");
    select.addEventListener("change", () => {
        const btnSubmit = document.getElementById("submit_new_freq");
        btnSubmit.click();
    })
}
var displayInput;

function calculatorEventRegistration() {
    displayInput = document.getElementById("display_input");
    const buttons = document.querySelector("#calculator-buttons").querySelectorAll("button");
    buttons.forEach(btn => {
        let nonDisplay = ["equals", "clear", "backspace"]
        if (nonDisplay.indexOf(btn.dataset.value) > -1) {
            if (btn.dataset.value == "equals") {
                btn.addEventListener("click", handleComputation)
            }
            else if (btn.dataset.value == "clear") {
                btn.addEventListener("click", clearDisplayInput)
            }
            else if (btn.dataset.value == "backspace") {
                btn.addEventListener("click", performBackSpace)
            }
        }  
        else {
            btn.addEventListener("click", handleDisplayValue)
        }
    })
}

function handleComputation() {

}

function clearDisplayInput() {
    displayInput.value = "0"
}

function performBackSpace() {
    displayInput.value = displayInput.value.slice(0, -1)
}

function handleDisplayValue() {
    if (displayInput.value == "0") {
        displayInput.value = ""
    }
    displayInput.value += this.dataset.value;
}

function start() {
    calculatorEventRegistration();
    submitFrequencyForm();
}

window.addEventListener("load", start)