import kotlinx.coroutines.*

fun main() = runBlocking {
    launch {
        delay(1000L)
        println("Фоновая задача завершена!")
    }
    println("Основной код продолжает работать...")
}