import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

fun getProgressFlow(): Flow<Int> = flow {
    for (i in 1..3) {
        delay(500L)
        emit(i * 33)
    }
    emit(100)
}

fun main() = runBlocking {
    getProgressFlow().collect { progress ->
        println("Загружено: $progress%")
    }
}