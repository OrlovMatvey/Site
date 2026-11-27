const addBtn = document.getElementById('addIngredientBtn');
const selector = document.getElementById('ingredientSelector');
const container = document.getElementById('ingredientsContainer');

addBtn.addEventListener('click', () => {
    const selectedValue = selector.value;
    // Получаем человеческое название из атрибута data-name
    const selectedName = selector.options[selector.selectedIndex].getAttribute('data-name');

    if (!selectedValue) {
        alert('Пожалуйста, выберите ингредиент из списка!');
        return;
    }

    if (container.querySelector(`[data-id="${selectedValue}"]`)) {
        alert('Этот ингредиент уже добавлен в список!');
        return;
    }

    // Создаем обертку для новой строки формы
    const row = document.createElement('div');
    row.className = 'ingredient-row';
    row.setAttribute('data-id', selectedValue);

    // Конструируем HTML из скрытого ID, названия и двух новых полей
    // Используем квадратные скобки [] в именах (name="...[]"), чтобы FastAPI принял их как список
    row.innerHTML = `
        <input type="hidden" name="ingredient_ids" value="${selectedValue}">
        <span class="ingredient-name">${selectedName}</span>
        
        <input type="number" name="ingredient_volumes" placeholder="Объем / Кол-во" required min="0" step="0.1">
        
        <select name="ingredient_units" required>
            <option value="г">г</option>
            <option value="кг">кг</option>
            <option value="мл">мл</option>
            <option value="л">л</option>
            <option value="шт">шт</option>
            <option value="ч. л.">ч. л.</option>
            <option value="ст. л.">ст. л.</option>
        </select>
        
        <button type="button" class="btn-remove-row">&times;</button>
    `;

    // Добавляем строку в контейнер
    container.appendChild(row);

    // Сбрасываем селект на значение по умолчанию
    selector.value = "";

    // Навешиваем событие удаления на крестик внутри созданной строки
    row.querySelector('.btn-remove-row').addEventListener('click', () => {
        row.remove();
    });
});
const modal = document.getElementById('recipeModal');
const openBtn = document.getElementById('openModalBtn');
const closeBtn = document.getElementById('closeModalBtn');

// Открыть модальное окно
openBtn.addEventListener('click', (e) => {
    e.preventDefault(); // Отменяем переход по ссылке #
    modal.showModal();
});

// Закрыть модальное окно при клике на крестик
closeBtn.addEventListener('click', () => {
    modal.close();
});

// Закрыть модальное окно при клике на серый фон вокруг
modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.close();
    }
});

function showModal(card) {
    document.getElementById("modalIngredients2").textContent = ""
    document.getElementById("modalTitle2").textContent = card.dataset.title;
    document.getElementById("modalCategory2").textContent = "🏷️ " + card.dataset.category;
    for (const element of card.dataset.ingredients){
        if (element!="'" && element!="{" && element!="}"){
            document.getElementById("modalIngredients2").textContent += element
        }
    }
    document.getElementById("likeButton").dataset.id = card.dataset.id;
    document.getElementById("dislikeButton").dataset.id = card.dataset.id;
    document.getElementById("exportButton").href = "/Service/Export/"+card.dataset.id
    document.getElementById("modalText2").textContent = card.dataset.body;
    document.getElementById("modalImage2").src = card.querySelector("img").src;

    document.getElementById("recipeModal2").style.display = "flex";
}

function closeModal() {
    document.getElementById("recipeModal2").style.display = "none";
}

const likeBut = document.getElementById("likeButton")
const dislikeBut = document.getElementById("dislikeButton")
likeBut.addEventListener("click", async (e) => {
    e.preventDefault();
    const data = {}
    data["is_like"]=true
    const url = "/Service/Reaction/"+likeBut.dataset.id
    try{
        const response = await fetch(url, {
            method: "POST",
            body: JSON.stringify(data)
        });
    }
    catch (error) {
        console.log(error)
    }
})
dislikeBut.addEventListener("click", async (e) => {
    e.preventDefault();
    const data = {}
    data["is_like"]=false
    const url = "/Service/Reaction/"+dislike.dataset.id
    try{
        const response = await fetch(url, {
            method: "POST",
            body: JSON.stringify(data)
        });
    }
    catch (error) {
        console.log(error)
    }
})