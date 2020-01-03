from django import forms
from django.contrib.auth import authenticate, get_user_model
from accounts import messages
from accounts.models import User, UserSecurityToken
from app.validations import validate_password
from app.decorators import anonymous_only, anonymous_view

class SignupForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    terms = forms.BooleanField(required=True,error_messages={'required': messages.TERMS_VALIDATION},widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ('first_name','last_name', 'email','password','terms') 

    def __init__(self, request=None, *args, **kwargs):
        self._token = None
        self._user_cache = None
        self.request = request

        super(SignupForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        try:
            get_user_model().objects.get(
                email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(messages.USER_WITH_THIS_MAIL_ALREADY_EXISTS,code='already_exist')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        self.request.session['user_email'] = user.email
        if commit:
            user.save()

                       
        self._token = UserSecurityToken.create_activation_token(
            user.email,user)
        self._token.send_verify_token_email(self.request)

        user.set_password(self.cleaned_data['password'])
        user.save()

        return user        


class LoginForm(forms.ModelForm):

    email = forms.EmailField(label=("Email"),
                             required=True,
                             error_messages={
                                 'required': messages.USER_EMPTY_EMAIL_VALIDATION,
                                 'invalid': messages.INVALID_EMAIL_ADDRESS})    

    password = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput,
        error_messages={'required': messages.USER_EMPTY_PASSWORD_VALIDATION})

        
    error_messages = {
        'invalid_login': messages.USER_INVALID_EMAIL_PASSWORD,
        'inactive': messages.USER_ACCOUNT_NOT_ACTIVE,
        'not_verified' :messages.USER_ACCOUNT_NOT_VERIFIED
    }

    class Meta:
        model = User
        fields = ('email', 'password')

    def __init__(self, request=None, *args, **kwargs):
        '''
        Initiatizes form with request and user_cache objects
        '''
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)
        user_model = get_user_model()
        self.username_field = user_model._meta.get_field(
            user_model.USERNAME_FIELD)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user_model = get_user_model()
            try:
                user = user_model._default_manager.get(email__iexact=email)
                if user.check_password(password):
                    self.user_cache = user
                if user.is_superuser or user.is_staff:
                    self.user_cache = None
            except user_model.DoesNotExist:
                self.user_cache = None
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': self.username_field.verbose_name},
                )
            elif not self.user_cache.is_verified:
                raise forms.ValidationError(
                    self.error_messages['not_verified'],
                    code="not_active")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data 

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache