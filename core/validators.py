from abc import ABC, abstractclassmethod
from  django.core import validators
from django.conf import settings
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.exceptions import APIException, ValidationError



name_no_numbers_symbols = validators.RegexValidator(
    regex = settings.NAME_ONLY_CHARS_DASH_UNDERSOCER,
    message='Name can contain only (letters - or _ )'
)

phone_with_plus = validators.RegexValidator(
    regex = settings.PHONE_VALIDATOR,
    message="phone only from 11 to 20 numbers with no letters (+) allowed "
)


class ValidateContract(ABC):
    '''
        Interface for validate class
    '''
    @abstractclassmethod
    def _validate(self, fields): ...


#TODO::Reactor
class Validate(ValidateContract):
    '''
        Validate logic for incoming fields
    '''
    @classmethod
    def _validate_pk(cls, pk):
        cls._validate_not_empty(pk)

    @classmethod
    def _validate_name(cls, name):
        cls._validate_not_empty(name)
        name_no_numbers_symbols(name)

    @classmethod
    def _validate_email(cls, email):
        cls._validate_not_empty(email)
        validators.validate_email(email)
    
    @classmethod
    def _validate_phone(cls, phone):
        cls._validate_not_empty(phone)
        phone_with_plus(phone)
    
  

    @classmethod
    def _validate_not_empty(cls, value):
        if not value:
            raise ValidationError(f'{value} is required.')

    @classmethod
    def _validate(cls, fields):
        '''
            Trigger for validations
        '''
        for field in fields:
            cls._validate_field(field, fields[field])

    @classmethod
    def _validate_field(cls, field, value):
        '''
            Execute a validation on a field
        '''
        method_name = cls._get_validator(field)
        if method_name:
            method_name(value)

    @classmethod
    def _get_validator(cls, field):
        '''
            Retrive a validator method using the field name
        '''
        method_name = cls._get_validator_by_field(field)
        return getattr(cls, method_name, None)

    @classmethod
    def _get_validator_by_field(cls, field):
        '''
            Generate a validator method name
        '''
        return f"_validate_{field}"
   
    
class ValidatePersonSubClass(Validate):
    '''
        Client for excuting a validation and or extra logic
    '''

    @classmethod
    def validate(cls, fields, skip_fields = None, nullable_fields = None):
        '''
            validates required fileds for a parson subclass
        '''
        if skip_fields:
            fields = cls._skip_fields(fields, skip_fields)
        cls._validate(fields)

    @classmethod
    def _skip_fields(cls, fields, skip_fields):
        '''
            Skip/edit  some passed fields
        '''
        return {
            field: fields.get(field)
            for field in fields
            if field not in skip_fields  
        }
