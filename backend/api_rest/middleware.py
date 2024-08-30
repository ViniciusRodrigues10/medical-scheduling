from .singleton.singleton import RequestLogger


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = RequestLogger()
        logger.log(f"Starting request: {request.path}")
        response = self.get_response(request)
        logger.log(f"Finished request: {request.path}")
        logger.save_log_to_file()
        logger.clear_log()
        return response
