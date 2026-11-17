document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const currentTable = urlParams.get('table') || 'users';

    // ЛОГИКА УДАЛЕНИЯ
    document.querySelectorAll(".btn-delete").forEach(button => {
        button.addEventListener("click", async (e) => {
            const rowId = button.getAttribute("data-id");         
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
    const modal = document.getElementById("editModal");
    const editForm = document.getElementById("editForm");
    const container = document.getElementById("formFieldsContainer");
    let activeRowId = null
    
    // Модальное окно
    document.querySelectorAll(".btn-edit").forEach(button => {
        button.addEventListener("click", (e) => {
            const row = button.closest("tr");
            activeRowId = button.getAttribute("data-id"); 
            const fields = container.querySelectorAll('input')
            fields.forEach(field => {
                const cell = row.querySelector(`td[data-name="${field.name}"]`)
                const value = cell.textContent.trim();
                field.value = value
            })
            const formData = new FormData(editForm);
            console.log(formData.entries())
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
            const response = await fetch(`/Admin/${currentTable}/${activeRowId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (response.ok){
                alert("Данные успешно сохранены!");
                window.location.reload();
            }
        } catch (error) {
            alert("Ошибка при отправке данных на сервер");
        }
    });
});