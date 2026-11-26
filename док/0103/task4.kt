import kotlinx.coroutines.*

suspend fun fetchDataFromNetwork(): String = withContext(Dispatchers.IO) {
    delay(1000L)
    "Данные с сервера"
}

fun main() = runBlocking {
    val data = fetchDataFromNetwork()
    println("Получено: $data")
}