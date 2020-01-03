from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager,PermissionsMixin
)
from django.conf import settings
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from justeece.core.utils import TimestampedModel
from app.string import Hash
from app.email import Email
from accounts import messages
# Create your models here.


class UserManager(BaseUserManager):
    '''
    User Custom Manager
    '''
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email):
        """
        Creates and saves a superuser.
        """
        user = self.create_user(email=email,password=password,)
        user.is_staff = True
        user.is_verified = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin, TimestampedModel):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30,blank=False )
    last_name = models.CharField(max_length=30, blank=False,null=True)
    is_staff = models.BooleanField(default=False) # staff user non superuser
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) 
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' #username

    objects = UserManager()


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        '''
        Saves the current instance. Override this in a subclass if you want to
        control the saving process.
        The 'force_insert' and 'force_update' parameters can be used to insist
        that the "save" must be an SQL insert or update (or equivalent for
        non-SQL backends), respectively. Normally, they should not be set.
        '''
        return super(User, self).save(force_insert=False,
                                      force_update=False,
                                      using=None,
                                      update_fields=None)

    USERNAME_FIELD = 'email'    
    objects = UserManager()

    def __str__(self):
        _ = self.__class__

        if self.first_name and self.last_name:
            return self.first_name +' '+self.last_name
        else:
            self.first_name =''
            self.last_name = ''
            return self.first_name +' '+self.last_name

    def get_short_name(self):
        _ = self.__class__
        return self.first_name

    class Meta(object):
        ''' User Class Meta '''
        verbose_name = ('User')
        verbose_name_plural = ('Users')

class UserSecurityToken(models.Model):
    '''
    User Security Token
    '''
    FORGOT_PASSWORD = 1
    ACCOUNT_ACTIVATION_TOKEN = 2
    TOKEN_TYPE_CHOICE = (
        (FORGOT_PASSWORD, ('Forgot Password')),
        (ACCOUNT_ACTIVATION_TOKEN, ('Account Activation Link'))
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, blank=True, on_delete=models.CASCADE, related_name='tokens')
    extras = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=150)
    token_type = models.SmallIntegerField(choices=TOKEN_TYPE_CHOICE)
    expire_date = models.DateTimeField()

    def __str__(self):
        if self.user:
            return self.user.email
        return self.extras

    @property
    def encoded_token(self):
        ''' Encoded token '''
        return Hash.encrypt_string(self.token).decode('utf-8')

    @staticmethod
    def create_token(expiry_date, token_type, user=None, extras=None):
        '''
        Create Token
        '''
        token = Hash.createhashforstring(user.email)
        data = {
            'user': user,
            'extras': extras,
            'token': token,
            'token_type': token_type,
            'expire_date': expiry_date
        }

        return UserSecurityToken.objects.create(**data)

    @staticmethod
    def create_forgot_password_token(user):
        ''' Forgot Password '''

        expire = timezone.now() + timezone.timedelta(**settings.ACCOUNT_VERIFY_TOKEN_EXPIRE_IN)
        UserSecurityToken.objects.filter(user=user,
                                         expire_date__gte=timezone.now(),
                                         token_type=UserSecurityToken.FORGOT_PASSWORD).update(expire_date=timezone.now())
        return UserSecurityToken.create_token(expire, UserSecurityToken.FORGOT_PASSWORD, user=user, extras=user.email)

    @staticmethod
    def create_activation_token(email, user):
        ''' Activation Token '''
        UserSecurityToken.objects.filter(user=user,
                                         extras=email,
                                         expire_date__gte=timezone.now(),
                                         token_type=UserSecurityToken.ACCOUNT_ACTIVATION_TOKEN).update(expire_date=timezone.now())
        expire = timezone.now() + timezone.timedelta(**settings.ACCOUNT_VERIFY_TOKEN_EXPIRE_IN)
        token = UserSecurityToken.create_token(
            expire, UserSecurityToken.ACCOUNT_ACTIVATION_TOKEN, user=user, extras=email)
        return token

    def send_verify_token_email(self, request):
        ''' Verify TOken '''
        encrypt_email = Hash.encrypt_string(self.extras)
        verification_path = reverse_lazy('accounts:email_confirmation', kwargs={
            'token': self.token,
            'id': encrypt_email.decode('utf-8')})

        verification_link = '%s://%s/%s' % (request.scheme,
                                            request.get_host(), verification_path[1:])
        Email(self.extras, messages.SUBJECT_ACCOUNT_ACTIVATION).message_from_template('accounts/email/account_confirmation.html',
                                                                                     {'verifyurl': verification_link, },
                                                                                     request).send()
        return self

    def send_forgot_password_email(self, request, emailtype):
        '''  Forgot Password Email '''
        encrypt_email = Hash.encrypt_string(self.user.email)
        changepassword_path = reverse_lazy('accounts:resetpassword', kwargs={
            'emailtype': emailtype,
            'token': self.token,
            'id': encrypt_email.decode('utf-8')})

        changepassword_link = '%s://%s/%s' % (request.scheme, request.get_host(),
                                              changepassword_path[1:])

        emailtemplate = 'accounts/email/change_password.html'
        subject = messages.SUBJECT_FORGOT_PASSWORD
        if not self.user.fb_id and not self.user.linkedin_id and not self.user.google_id:
            Email(self.user.email,
                subject
                ).message_from_template(emailtemplate,
                                        {'changepassword_link': changepassword_link,
                                        'first_name': self.user.first_name,
                                        'last_name': self.user.last_name},
                                        request
                                        ).send()
        return self