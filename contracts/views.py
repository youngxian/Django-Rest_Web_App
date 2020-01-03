from django.shortcuts import render
from django.views.generic import View, FormView, TemplateView, CreateView
from django.urls import reverse
from accounts.models import User
from contracts.forms import CreateContractForm, CreateContractTypeForm
from contracts.models import ContractsModel,ContractTypeModel
from django.urls import reverse_lazy
# Create your views here.

class CreateContractTypeView(CreateView):

    form_class = CreateContractTypeForm
    template_name = 'contracts/contract_type.html'
    
    def get_success_url(self):
        return reverse_lazy( 'contracts:successview') 
    
class SuccessView(TemplateView):
    
    template_name = 'contracts/success.html'

class RenderContractType(TemplateView):
    
    template_name = 'contract'

class SubmitContract(View):
    
    def get(self,request,**args):
        try:
            contract_id = self.kwargs['contract_id']
            
            contract = ContractsModel.objects.get(id=contract_id)
            contract.status = ContractsModel.IN_PROGRESS
            contract.save()
            return render(request,'accounts/contract_completion.html',{"email":contract.created_with_email})  
        except Exception as e:
            return render(request,'accounts/error.html') 

class CreateContractView(View):
    
    def get(self,request,**args):
        try:
            search = request.GET.get('search')
            user_id = None
            form = CreateContractForm
            if search:
                user = User.objects.filter(email=search)
                if user:
                    user_id = user[0].id
                    
            contracts_type = list(ContractTypeModel.objects.all().values('id','name'))
            return render(request,'contracts/create_contract.html',{"email":search,user_id:user_id, "contract_type":contracts_type,"form":form})  
        except Exception as e:
            return render(request,'contracts/create_contract.html') 
    
    
    def post(self, request):
        try:
          
            tempdict = self.request.POST.copy()
            tempdict['created_by'] = request.user.id
            
            form = CreateContractForm(tempdict)
      
            if 'payment_included' in tempdict:
                payment_included = tempdict.get('payment_included')
            else:
                payment_included = False

            if 'amount' in tempdict:
                if tempdict.get('amount') =='':
                    amount = 0
                else:
                    amount = tempdict.get('amount')
            else:
                amount = 0

            contaract_type_id = ContractTypeModel.objects.get(name=tempdict.get('contract_type'))
            instance                = form.save(commit=False)
            instance.created_by     = User.objects.get(id=request.user.id)
            instance.contract_type  = contaract_type_id
            instance.contract_start_date     = tempdict.get('contract_start_date')
            instance.contract_end_date       = tempdict.get('contract_end_date') 
            instance.summary                 = tempdict.get('summary')
            instance.amount                  = amount
            instance.payment_included        = payment_included
            instance.status                  = ContractsModel.DRAFT
            instance.created_with            = tempdict.get('created_with')
            instance.created_with_email      = tempdict.get('created_with_email')
            instance.subcategory             = tempdict.get('subcategory')
            instance.save()
            
            tempdict['id']      = instance.id
            tempdict['status']  = ContractsModel.DRAFT
            send_data = {"contract":tempdict}
            return render(request,'contracts/contract_confirmation.html',send_data)  
        except Exception as e:
            print(str(e))
            return render(request,'contracts/create_contract.html')  

class EditContractView(View):
    
    def get(self,request,**kwargs):
        try:
            contract_id = self.kwargs['contract_id']
            contract = ContractsModel.objects.get(id=contract_id)
            contracts_type = list(ContractTypeModel.objects.all().values('id','name'))
            data = {
                "email"         :contract.created_with_email,
                "contract_type" :contract.contract_type.name,
                "subcategory"   :contract.subcategory,
                "contract_start_date":contract.contract_start_date,
                "contract_end_date"  :contract.contract_end_date,
                "summary"       : contract.summary,
                "payment_included": contract.payment_included,
                "amount"          : contract.amount
            }
            form = CreateContractForm(initial=data)
           
            return render(request,'contracts/create_contract.html',{"email":data["email"],"selected_contract":data["contract_type"],"contract_type":contracts_type, "form":form})  
        except Exception as e:
            return render(request,'contracts/create_contract.html') 

class ContractConfirmationView(TemplateView):
    template_name = 'contracts/contract_confirmation.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        contract = ContractsModel.objects.get(id=self.kwargs['contract_id'])
        try:
            context['contract'] = contract
        except:
            pass
        return context

class ContractCompletionView(TemplateView):
    template_name = 'accounts/contract_completion.html'
