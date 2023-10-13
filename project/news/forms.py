from .models import New
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea

class NewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'вы не выбрали категорию'

    class Meta:
        model = New
        fields = ['title', 'text',  'category']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Название публикации'}),
            'datе': DateTimeInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Дата публикации'}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст публикации'}),
            'category__title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Категория'})
        }


def clean(self):
    cleaned_data = super().clean()
    text = cleaned_data.get("text")
    if text is not None and len(text) < 20:
        raise ValidationError({
            "text": "Описание не может быть менее 20 символов."
        })

    return text