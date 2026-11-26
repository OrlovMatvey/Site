fun main() {
    val tasks = mutableListOf<String>()
    var isRunning = true

    while (isRunning) {
        println("\n--- TODO ЛИСТ ---")
        println("1. Посмотреть список задач")
        println("2. Добавить задачу")
        println("3. Удалить задачу")
        println("4. Выход")
        print("Выберите действие (1-4): ")

        when (readlnOrNull()?.trim()) {
            "1" -> {
                if (tasks.isEmpty()) {
                    println("Список задач пуст.")
                } else {
                    println("\nВаши задачи:")
                    tasks.forEachIndexed { index, task ->
                        println("${index + 1}. $task")
                    }
                }
            }
            "2" -> {
                print("Введите текст задачи: ")
                val task = readlnOrNull()?.trim()
                if (!task.isNullOrEmpty()) {
                    tasks.add(task)
                    println("Задача добавлена")
                } else {
                    println("Задача не может быть пустой.")
                }
            }
            "3" -> {
                if (tasks.isEmpty()) {
                    println("Нечего удалять, список пуст.")
                    continue
                }
                print("Введите номер задачи для удаления: ")
                val indexInput = readlnOrNull()?.toIntOrNull()
                if (indexInput != null && indexInput in 1..tasks.size) {
                    val removed = tasks.removeAt(indexInput - 1)
                    println("Удалена задача: \"$removed\"")
                } else {
                    println("Неверный номер задачи.")
                }
            }
            "4" -> {
                println("До свидания")
                isRunning = false
            }
            else -> {
                println("Неверный выбор. Попробуйте снова.")
            }
        }
    }
}