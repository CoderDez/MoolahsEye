function getCategories() {
    lookup = {}
    const cats = document.querySelectorAll(".category");
    cats.forEach(cat => {
        lookup[cat.dataset.name] = cat.dataset.cost;
    })
    return lookup;
}

const categories = getCategories()
console.log(categories);

new Chart(document.getElementById('pie_chart'), {
    type: 'pie',
    data: {
    labels: Object.keys(categories),
    datasets: [{
        data: Object.values(categories)
    }]
    },
    options: {
        reponsive: true
    }
}); 
