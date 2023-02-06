class InvalidFrequencyException(Exception):
    def __str__(self):
        return "Value for frequency is invalid."

class FrequencyExceedanceException(Exception):
    def __str__(self):
        return "Item frequency can not exceed Budget frequency."

class InsufficientBudgetAmountException(Exception):
    def __str__(self):
        return "The Budgets amount is not sufficient to handle the cost of all its items."

class NegativeValueException(Exception):
    def __str__(self):
        return "Negative value is not permitted."

class ImpermissibleItemCostException(Exception):
    def __str__(self):
        return "The Item's cost has caused Budget's costs to exceed its amount."
    
class UniqueNameValueException(Exception):
    def __str__(self):
        return "The Item's name was not unique within its Budget item_set."