from django.db import models
import ast

class ListField(models.TextField):
    """
    Taken from: 
    http://stackoverflow.com/questions/5216162/how-to-create-list-field-in-django
    """
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class Node(models.Model):
    id = models.CharField()
    name = models.CharField()
    description = models.CharField()
    address = models.CharField()
    email = models.CharField()
    tor2web_admin = models.BooleanField()
    tor2web_receiver = models.BooleanField()
    tor2web_submission = models.BooleanField()
    tor2web_unauth = models.BooleanField()
    default_language = models.CharField()
    supported_languages = ListField()
    last_updated = models.DateField(auto_now=True)
