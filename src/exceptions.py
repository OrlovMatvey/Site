#Доделать
class AppException(Exception):
    status_code = 400
    detail = "Произошла ошибка"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class NotFoundError(AppException):
    status_code = 404
    detail = "Не удалось найти запрашиваемый ресурс"


class AccessError(AppException):
    status_code = 403
    detail = "Недостаточно прав доступа"


class IncorrectInput(AppException):
    status_code = 400
    detail = "Некорректный ввод"

class UnauthorizedError(AppException):
    status_code = 401
    detail = "Требуется авторизация"

class ConflictError(AppException):
    status_code = 409
    detail = "Данный email уже занят"