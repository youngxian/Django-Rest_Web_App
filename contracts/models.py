from django.db import models
from justeece.core.utils import TimestampedModel
from accounts.models import User
# Create your models here.

class ContractTypeModel(TimestampedModel):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name    


class ContractsModel(TimestampedModel):

    DRAFT = 1
    PENDING = 2
    IN_PROGRESS = 3
    COMPLETED = 4
    CANCELED = 5
    DISPUTE = 6

    CONTRACT_STATUS_CHOICES = (
        (DRAFT, ('Forgot Password')),
        (PENDING, ('Account Activation Link')),
        (IN_PROGRESS, ('In Progress')),
        (COMPLETED, ('Completed')),
        (CANCELED, ('Canceled')),
        (DISPUTE, ('Dispute'))
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by_user")
    created_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_with_user", null=True, blank=True)
    created_with_email = models.EmailField(null=True, blank=True) 
    contract_type = models.ForeignKey(ContractTypeModel, on_delete=models.CASCADE, related_name="create_contract_type")
    subcategory = models.CharField(max_length=100)
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    summary = models.TextField(max_length=500)
    payment_included = models.BooleanField(default=False)
    amount = models.BigIntegerField(null=True, blank=True)
    status = models.SmallIntegerField(choices=CONTRACT_STATUS_CHOICES, default=DRAFT)

    class Meta:
        db_table = "create_contract"
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return str(self.created_by.first_name)