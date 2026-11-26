import kotlinx.coroutines.*

fun main() = runBlocking {
    val result = withTimeoutOrNull(1000L) {
        delay(2000L)
        "Успех"
    }
    println("Результат: $result") // Выведет: Результат: null
}