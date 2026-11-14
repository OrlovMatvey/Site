document.addEventListener("DOMContentLoaded", () => {
    // Получаем имя текущей таблицы из URL параметров (например, ?table=tokens)
    const urlParams = new URLSearchParams(window.location.search);
    const currentTable = urlParams.get('table') || 'users';

    // === ЛОГИКА УДАЛЕНИЯ ===
    document.querySelectorAll(".btn-delete").forEach(button => {
        button.addEventListener("click", async (e) => {
            const rowId = button.getAttribute("data-id");
            
            if (confirm(`Вы уверены, что хотите удалить запись #${rowId}?`)) {
                try {
                    const response = await fetch(`/Admin/${currentTable}/${rowId}`, {
                        method: "DELETE"
                    });
                    
                    const result = await response.json();
                    if (response.ok && result.status === "success") {
                        // Находим строку таблицы <tr> и плавно удаляем её из HTML
                        button.closest("tr").remove();
                    } else {
                        alert("Ошибка при удалении: " + (result.detail || "Неизвестная ошибка"));
                    }
                } catch (error) {
                    alert("Не удалось связаться с сервером");
                }
            }
        });
    });

    // === ЛОГИКА ИЗМЕНЕНИЯ (МОДАЛЬНОЕ ОКНО) ===
    const modal = document.getElementById("editModal");
    const editForm = document.getElementById("editForm");
    const container = document.getElementById("formFieldsContainer");
    let activeRowId = null;

    document.querySelectorAll(".btn-edit").forEach(button => {
        button.addEventListener("click", (e) => {
            activeRowId = button.getAttribute("data-id");
            const row = button.closest("tr");
            container.innerHTML = ""; // Очищаем старые поля формы

            // Собираем все данные из текущей строки таблицы
            // Браузер пробежится по ячейкам <td> и создаст input под каждое поле
            const headers = Array.from(document.querySelectorAll(".db-table th")).map(th => th.innerText.toLowerCase());
            const cells = Array.from(row.querySelectorAll("td"));

            headers.forEach((header, index) => {
                if (header === "действия") return; // Кнопки не редактируем
                
                const cellValue = cells[index].getAttribute("title") || cells[index].innerText.trim();

                const fieldWrapper = document.createElement("div");
                fieldWrapper.style.marginBottom = "12px";

                const label = document.createElement("label");
                label.innerText = header.toUpperCase();
                label.style.display = "block";
                label.style.marginBottom = "4px";
                label.style.fontWeight = "bold";

                const input = document.createElement("input");
                input.name = header;
                input.value = cellValue;
                input.style.width = "100%";
                input.style.padding = "6px";
                input.style.boxSizing = "border-box";
                input.style.padding = "10px";
                input.style.border = "1px solid #ccc";
                input.style.borderRadius = "6px";
                input.style.fontFamily = "inherit";
                input.style.fontSize = "1rem";

                // Запрещаем редактировать ID
                if (header === "id") {
                    input.disabled = true;
                    input.style.backgroundColor = "#e9ecef";
                }

                fieldWrapper.appendChild(label);
                fieldWrapper.appendChild(input);
                container.appendChild(fieldWrapper);
            });

            modal.style.display = "block"; // Показываем модальное окно
        });
    });

    // Закрытие модального окна
    const closeModal = () => { modal.style.display = "none"; };
    document.querySelector(".close-modal").addEventListener("click", closeModal);
    document.getElementById("cancelEditBtn").addEventListener("click", closeModal);

    // Отправка измененных данных на сервер
    editForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(editForm);
        const data = {};
        
        // Превращаем данные формы в обычный JSON-объект
        formData.forEach((value, key) => {
            // Приведение строковых "Да/Нет" к булевым значениям для БД
            if (value.toLowerCase() === "да") value = true;
            if (value.toLowerCase() === "нет") value = false;
            data[key] = value;
        });

        try {
            const response = await fetch(`/Admin/${currentTable}/${activeRowId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            if (response.ok && result.status === "success") {
                alert("Данные успешно сохранены!");
                window.location.reload(); // Перезагружаем страницу, чтобы увидеть изменения из БД
            } else {
                alert("Ошибка сохранения: " + (result.detail || "Неизвестная ошибка"));
            }
        } catch (error) {
            alert("Ошибка при отправке данных на сервер");
        }
    });
});