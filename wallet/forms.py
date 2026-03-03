from django import forms
from .models import Deposit


class DepositForm(forms.ModelForm):

    # 🔥 여기서 재정의
    deposit_value = forms.CharField()

    class Meta:
        model = Deposit
        fields = ("deposit_value", "deposit_name")

    def clean_deposit_value(self):
        value = self.cleaned_data["deposit_value"]

        # 콤마 제거
        value = value.replace(",", "")

        try:
            value = int(value)
        except ValueError:
            raise forms.ValidationError("숫자만 입력하세요.")

        if value <= 10000:
            raise forms.ValidationError("10,000원 이상 입력하세요.")

        return value
