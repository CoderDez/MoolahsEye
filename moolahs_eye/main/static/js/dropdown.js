// function to register functionality for dropdown
function dropdown() {
    const dropdowns = document.querySelectorAll(".dropdown");

    dropdowns.forEach(dd => {
        const select = dd.querySelector(".select");
        const caret = dd.querySelector(".caret");
        const menu = dd.querySelector(".menu");
        const options = dd.querySelectorAll(".menu li");
        const selected = dd.querySelector(".selected");

        select.addEventListener("click", () => {
            select.classList.toggle("select-clicked");
            caret.classList.toggle("caret-rotate");
            menu.classList.toggle("menu-open");

            const selectElems = document.querySelectorAll(".select");
            selectElems.forEach(sel => {
                if (sel.classList.contains("select-clicked") && sel != select) {
                    sel.click();
                }
            })
        })

        options.forEach(opt => {
            opt.addEventListener("click", () => {
                selected.innerText = opt.innerText
                select.classList.remove("select-clicked");
                caret.classList.remove("caret-rotate");
                menu.classList.remove("menu-open");

                options.forEach(opt => {
                    opt.classList.remove("active");
                })
                opt.classList.add("active");

                // reset the records
                if (document.querySelector(".reports-form")) {
                    removeRecords();
                }
            })
        })
    })
}


// function to register functionality for dropdown with checkboxes
function dropdownCheckbox() {
    const dropdowns = document.querySelectorAll(".dropdown-checkbox");
    dropdowns.forEach(dd => {
        const select = dd.querySelector(".select");
        const caret = dd.querySelector(".caret");
        const menu = dd.querySelector(".menu");

        select.addEventListener("click", () => {
            select.classList.toggle("select-clicked");
            caret.classList.toggle("caret-rotate");
            menu.classList.toggle("menu-open");
            menu.classList.toggle("dropdown-checkbox-closed");
        })
    })
}