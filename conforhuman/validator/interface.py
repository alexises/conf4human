from conforhuman.ast import LocalizableObject

class ValidatorInterface(object):
    def validate(self, object: LocalizableObject) -> bool:
        '''
            validate : check attribute against validation
            Return True if validation is successfull
                   False if Validation is failled
        '''
        raise NotImplementedError("This class is an interface")

    def getError(self, object: LocalizableObject) -> str:
        '''
            getError : get descriptive validation error message
            Return error message relative to the issue
        '''
        raise NotImplementedError("This class is an interface")