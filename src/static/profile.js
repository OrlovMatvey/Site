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