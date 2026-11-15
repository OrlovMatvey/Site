    function showModal(card) {
        document.getElementById("modalTitle").textContent = card.dataset.title;
        document.getElementById("modalCategory").textContent = "🏷️ " + card.dataset.category;
        document.getElementById("modalText").textContent = card.dataset.body;
        document.getElementById("modalImage").src = card.querySelector("img").src;

        document.getElementById("recipeModal").style.display = "flex";
    }

    function closeModal() {
        document.getElementById("recipeModal").style.display = "none";
    }