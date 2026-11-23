
class AppException(Exception):
    status_code = 400
    detail = "Произошла ошибка"

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)


class NotFoundError(AppException):
    status_code = 404
    detail = "Не удалось найти запрашиваемый ресурс"


class PermissionError(AppException):
    status_code = 401
    detail = "Недостаточно прав доступа"