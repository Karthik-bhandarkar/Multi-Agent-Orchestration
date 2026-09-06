import sys


def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    Extracts the exact filename and line number where an exception
    occurred, using the traceback object from sys.exc_info().
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return f"Exception in [{file_name}] at Line [{line_number}]: {str(error)}"


class CustomException(Exception):
    """
    Enterprise exception wrapper that preserves full traceback context.
    Usage:
        try:
            risky_operation()
        except Exception as e:
            raise CustomException(e, sys) from e
    """

    def __init__(self, error: Exception, error_detail: sys):
        super().__init__(str(error))
        self.error_message = error_message_detail(error, error_detail)

    def __str__(self):
        return self.error_message
