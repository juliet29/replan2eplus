# from utils4plans.printing import StyledConsole

# TODO add rich styling?
class InvalidEpBunchException(Exception):
    def __init__(self, expected_key, actual_key):
        self.expected_key = expected_key
        self.actual_key = actual_key

    def __str__(self):
        return f"Expected an EpBunch with key `{self.expected_key}`, but instead got one with key `{self.actual_key}!"
