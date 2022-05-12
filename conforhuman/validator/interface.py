from conforhuman.ast import LocalizableObject

class ValidatorInterface(object):
    def validate(self, object: LocalizableObject) -> bool:
        '''
            validate : check attribute against validation
            Return True if validation is successfull
                   False if Validation is failled
        '''
        raise NotImplementedError("This class is an interface")