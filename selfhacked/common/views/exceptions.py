class RequestParamNotFound(Exception):
    def __init__(self, name):
        super().__init__(f"Parameter '{name}' not found")
        self.name = name
