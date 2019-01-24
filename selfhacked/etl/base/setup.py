class SetupCheck(object):
    class SetupError(Exception):
        pass

    def setup_check(self):
        raise NotImplementedError
