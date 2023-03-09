
function clickBudgetButtonAnchor() {
    const buttonsContainer = document.getElementById("budget-buttons");
    if (buttonsContainer) {
        buttonsContainer.querySelectorAll(".btn").forEach(btn => {
            btn.addEventListener("click", () => {
                // get the anchor elements id
                let anchorID = btn.id.split("btn_")[1];
                // click anchor
                document.getElementById(anchorID).click();
            })
        });
    }
}

function cancelBudgetForm() {
    const btnCancel = document.getElementById("btn_cancel_budget");
    if (btnCancel) {
        btnCancel.addEventListener("click", () => {
            document.getElementById("cancel_budget").click()
        })
    }
}

function clickItemButtonAnchor() {
    const buttonsContainer = document.getElementById("item_buttons");
    console.log(buttonsContainer);
    if (buttonsContainer) {
        buttonsContainer.querySelectorAll(".btn").forEach(btn => {
            btn.addEventListener("click", () => {
                console.log("??")
                let anchorID = btn.id.split("btn_")[1]
                document.getElementById(anchorID).click();
            })
        })
    }
}

function cancelItemForm() {
    const btnCancel = document.getElementById("btn_cancel_item");
    if (btnCancel) {
        btnCancel.addEventListener("click", () => {
            document.getElementById("cancel_item").click();
        })
    }
}


function start() {
    clickBudgetButtonAnchor();
    cancelBudgetForm();
    clickItemButtonAnchor();
    cancelItemForm();
}

window.addEventListener("load", start)