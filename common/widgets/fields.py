from django.db.models.fields.files import FileField

class BanzaiFileField(FileField):
    auto_delete = False
    def __init__(self, *args, **kwargs):
        if kwargs.get('auto_delete', None):
            self.auto_delete = kwargs.pop('auto_delete')

        super(BanzaiFileField, self).__init__(*args, **kwargs)
    
    def deconstruct(self):
        return super().deconstruct(self)