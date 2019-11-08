from django import forms
from main.models import Schedule, Cabinet


class ScheduleAdminForm(forms.ModelForm):
    class Meta:
        model = Schedule

        fields = '__all__'

    cabinet = forms.ModelChoiceField(
        queryset=Cabinet.objects.filter(auditoria=True).order_by('name'),
        empty_label=None)
