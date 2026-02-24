from django import forms
from .models import Item

class Item_form(forms.ModelForm):

    item_price = forms.CharField()
    delivery_1 = forms.CharField()
    delivery_2 = forms.CharField()

    class Meta:
        model = Item
        exclude = ["item_status"]

    def clean_price_field(self, field_name):
        value = self.cleaned_data.get(field_name)

        if not value:
            return 0

        value = value.replace(",", "")

        if not value.isdigit():
            raise forms.ValidationError("숫자만 입력해주세요.")

        return int(value)

    def clean_item_price(self):
        return self.clean_price_field("item_price")

    def clean_delivery_1(self):
        return self.clean_price_field("delivery_1")

    def clean_delivery_2(self):
        return self.clean_price_field("delivery_2")