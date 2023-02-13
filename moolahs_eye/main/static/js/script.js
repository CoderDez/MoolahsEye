
function frequencyInputChanger() {
    const frequencyDropdown = document.querySelector(".frequency-dropdown");
    const items = frequencyDropdown.querySelectorAll(".menu li");
    items.forEach(li => {
        li.addEventListener("click", () => {
            const freqInput = document.querySelector("#budget_frequency");
            freqInput.value = li.innerHTML;
        })
    })
}

function start() {

}

window.addEventListener("load", start);