import kotlinx.coroutines.*

suspend fun getUserName(): String {
    delay(1000L)
    return "Алексей"
}

suspend fun getUserBalance(): Int {
    delay(1500L)
    return 5000
}

fun main() = runBlocking {
    val nameDeferred = async { getUserName() }
    val balanceDeferred = async { getUserBalance() }
    
    println("Пользователь: ${nameDeferred.await()}, Баланс: ${balanceDeferred.await()} руб.")
}