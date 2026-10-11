from django import forms
from django.core.validators import RegexValidator
from .models import Inquiry

REQUEST_TYPES = ['企业存储采购', '存储扩容升级', '备份与容灾', '方案咨询', '其他需求']
BUDGETS = ['5万元以下', '5–20万元', '20–50万元', '50–100万元', '100万元以上', '待评估']


class InquiryForm(forms.ModelForm):
    phone = forms.CharField(max_length=30, validators=[RegexValidator(r'^[+0-9()\s-]{6,30}$', '请输入有效的联系电话。')])
    request_type = forms.ChoiceField(choices=[(x, x) for x in REQUEST_TYPES])
    budget = forms.ChoiceField(choices=[(x, x) for x in BUDGETS])
    quantity = forms.IntegerField(min_value=1, max_value=1000000)

    class Meta:
        model = Inquiry
        fields = ['contact', 'phone', 'company', 'request_type', 'quantity', 'city', 'budget', 'description']
