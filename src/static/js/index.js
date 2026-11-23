function showModal(card) {
    document.getElementById("modalIngredients2").textContent = ""
    document.getElementById("modalTitle2").textContent = card.dataset.title;
    document.getElementById("modalCategory2").textContent = "🏷️ " + card.dataset.category;
    for (const element of card.dataset.ingredients){
        if (element!="'" && element!="{" && element!="}"){
            console.log(element)
            document.getElementById("modalIngredients2").textContent += element
        }
    }
    document.getElementById("modalText2").textContent = card.dataset.body;
    document.getElementById("modalImage2").src = card.querySelector("img").src;

    document.getElementById("recipeModal2").style.display = "flex";
}

function closeModal() {
    document.getElementById("recipeModal2").style.display = "none";
}