
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
    if (buttonsContainer) {
        buttonsContainer.querySelectorAll(".btn").forEach(btn => {
            btn.addEventListener("click", () => {
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

var editStarted = false
function displayEditButtons() {
    const btnTrigger = document.getElementById("edit_item");
    const btnDone = document.getElementById("btn_item_edit_done");
    btnTrigger.addEventListener("click", displayEditButton);
    btnDone.addEventListener("click", displayEditButton)
}

function displayEditButton() {
    const btns = document.querySelectorAll(".btn-edit-item");
    if (editStarted) {
        btns.forEach(btn => {
            btn.classList.add("hider");
        })
        editStarted = false
        showItemEditDoneButton();
    }
    else {
        btns.forEach(btn => {
            btn.classList.remove("hider");
        })
        editStarted = true;
        showItemEditDoneButton();
    }
}

function showItemEditDoneButton() {
    const btnNew = document.getElementById("btn_new_item");
    const btnDropDown = document.querySelector(".btn-item-dropdown");
    const btnDone = document.getElementById("btn_item_edit_done");
    
    if (editStarted) {
        btnNew.classList.add("hider");
        btnDropDown.classList.add("hider");
        btnDone.classList.remove("hider")
    }
    else {
        btnNew.classList.remove("hider");
        btnDropDown.classList.remove("hider");
        btnDone.classList.add("hider")
    }
}

function chooseItemView() {
    const btnViews = document.querySelector(".table-functionality-buttons");
    if (btnViews) {
        btnViews.querySelectorAll("button").forEach(btn => {
            btn.addEventListener("click", () => {
                let sibling = btn.nextElementSibling;
                if (!sibling) {
                    sibling = btn.previousElementSibling;
                }
                btn.classList.add("items-view-chosen");
                sibling.classList.remove("items-view-chosen");
                
                const itemsTable = document.querySelector(".items-table")
                const dataBreakdown = document.querySelector(".data-breakdown");
                console.log(itemsTable);
                console.log(dataBreakdown);
                if (btn.id == "table_item_view") {
                    itemsTable.classList.remove("hider");
                    dataBreakdown.classList.add("hider")
                } 
                else if (btn.id == "chart_item_view") {
                    dataBreakdown.classList.remove("hider");
                    itemsTable.classList.add("hider");
                }
            })
        })
    }
}


function start() {
    cancelBudgetForm();
    clickItemButtonAnchor();
    cancelItemForm();
    displayEditButtons();
    chooseItemView();
}

window.addEventListener("load", start)