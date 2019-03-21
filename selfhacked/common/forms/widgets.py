from django.contrib.postgres.forms import SplitArrayWidget


class ArrayFieldWidget(SplitArrayWidget):
    template_name = 'selfhacked_common/array_field_widget.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        return [
            value
            for value in super().value_from_datadict(data, files, name)
            if value
        ]

    def get_context(self, name, value, attrs=None):
        value = (value or '').split(',')
        return super().get_context(name, value, attrs)
