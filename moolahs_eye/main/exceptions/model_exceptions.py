class FrequencyException(Exception):
    def __str__(self):
        return "Value for frequency is invalid."


class InsufficientAmountException(Exception):
    def __str__(self):
        return "The Budgets amount is not sufficient."