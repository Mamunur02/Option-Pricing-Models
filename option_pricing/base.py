from enum import Enum
class OPTION_TYPE(Enum):
    CALL_OPTION = 'Call Option'
    PUT_OPTION = 'Put Option'

# Class for interface of option pricing models
class OptionPricingModel():

    # Calculates call/put option
    def calculate_option_price(self, option_type):
        if option_type == OPTION_TYPE.CALL_OPTION.value:
            return self._calculate_call_option_price()
        elif option_type == OPTION_TYPE.PUT_OPTION.value:
            return self._calculate_put_option_price()
        else:
            return -1

    @classmethod
    def _calculate_call_option_price(self):
        pass

    @classmethod
    def _calculate_put_option_price(self):
        pass