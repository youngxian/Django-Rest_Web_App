import datetime
from django import forms

from contracts.models import ContractsModel, ContractTypeModel
from accounts.models import User

class CreateContractForm(forms.ModelForm):
   
    class Meta:
        model = ContractsModel

        fields = ['created_by', 'created_with_email', 'contract_type', 'subcategory', 'contract_start_date','contract_end_date', 'summary', 'payment_included', 'amount']

    def __init__(self, request=None, user=None, contract=None, *args, **kwargs):
        super(CreateContractForm, self).__init__(*args, **kwargs)
        
        self.fields['contract_type'].queryset = ContractTypeModel.objects.all()
    #     self.request = request
        # self.user = user
    #     self.contract = contract
        self.fields['contract_type'].empty_label = None

    # def clean_created_by(self):
    #     created_by = User.objects.get(id=self.user.id)
    #     return created_by

    # def clean(self):
       
    #     cleaned_data = super(CreateContractForm, self).clean()
    #     if cleaned_data['contract_end_date'] < cleaned_data['contract_start_date']:
    #         self.add_error('contract_start_date', "Contract's end date cannnot be greater than the start date. ")
    #     return cleaned_data

    # def save(self):
    #     if self.contract:
    #         ContractsModel.objects.filter(id=self.contract.id).update(**self.cleaned_data)
    #     else:
    #         ContractsModel.objects.create(**self.cleaned_data)
    #     return self
    
class CreateContractTypeForm(forms.ModelForm):
   
    name = forms.CharField(required=True)
    
    class Meta:
        model = ContractTypeModel
        fields = ['name']