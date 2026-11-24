document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const currentTable = urlParams.get('table') || 'User';
    const modal = document.getElementById("editModal");
    const editForm = document.getElementById("editForm");
    const container = document.getElementById("formFieldsContainer");
    let rowId = null

    // ДОБАВЛЕНИЕ ЗАПИСИ
    const openBtn = document.getElementById('openModalBtn');
    openBtn.addEventListener('click', (e) => {
        e.preventDefault(); // Отменяем переход по ссылке #
        modal.style.display = "flex";
    });

    // ЛОГИКА УДАЛЕНИЯ
    document.querySelectorAll(".btn-delete").forEach(button => {
        button.addEventListener("click", async (e) => {
            rowId = button.getAttribute("data-id");         
            if (confirm(`Вы уверены, что хотите удалить запись #${rowId}?`)) {
                try {
                    const response = await fetch(`/Admin/${currentTable}/${rowId}`, {
                        method: "DELETE"
                    });
                    if(response.ok){
                        button.closest("tr").remove();
                    }
                } catch (error) {
                    console.log("Не удалось связаться с сервером");
                }
            }
        });
    });

    // ЛОГИКА ИЗМЕНЕНИЯ
    
    // Модальное окно
    document.querySelectorAll(".btn-edit").forEach(button => {
        button.addEventListener("click", (e) => {
            const row = button.closest("tr");
            rowId = button.getAttribute("data-id"); 
            const fields = container.querySelectorAll('input')
            fields.forEach(field => {
                const cell = row.querySelector(`td[data-name="${field.name}"]`)
                const value = cell.textContent.trim();
                field.value = value
            })
            modal.style.display = "flex"; // Показываем модальное окно
        });
    });

    // Закрытие модального окна
    const closeModal = () => { modal.style.display = "none"; };
    document.querySelector(".close-modal").addEventListener("click", closeModal);
    document.getElementById("cancelEditBtn").addEventListener("click", closeModal);

    // Отправка данных на сервер в JSON формате
    editForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(editForm);
        const data = {};
        
        formData.forEach((value, key) => {
            if (value.toLowerCase() === "да"){value = true};
            if (value.toLowerCase() === "нет"){value = false};
            data[key] = value;
        });

        try {
            const response = await fetch(`/Admin/${currentTable}/${rowId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (response.ok){
                console.log("Данные успешно сохранены!");
                window.location.reload();
            }
        } catch (error) {
            console.log("Ошибка при отправке данных на сервер");
        }
    });
});