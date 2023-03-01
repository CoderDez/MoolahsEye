function toggleCreateNewBudget() {
    const btnNewBudget = document.querySelector(".btn-new-budget");
    btnNewBudget.addEventListener("click", () => {
        const btnSubmit = document.querySelector(".new-budget");
        btnSubmit.click();
    });
}

function start() {
    toggleCreateNewBudget();
}

window.addEventListener("load", start)