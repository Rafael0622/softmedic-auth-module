from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# -------------------------------------------------------------------
# FORMULARIO DE REGISTRO PERSONALIZADO
# -------------------------------------------------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['nombre', 'correo', 'rol', 'password1', 'password2']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre completo','autocomplete': 'off'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Correo electrónico','autocomplete': 'off'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if CustomUser.objects.filter(correo=correo).exists():
            raise forms.ValidationError("⚠️ Este correo ya está registrado.")
        return correo

# -------------------------------------------------------------------
# FORMULARIO DE INICIO DE SESIÓN PERSONALIZADO
# -------------------------------------------------------------------
class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Correo electrónico','autocomplete': 'off'})
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Contraseña'})
    )

# -------------------------------------------------------------------
# FORMULARIO DE SOLICITUD DE RECUPERACIÓN DE CONTRASEÑA
# -------------------------------------------------------------------
class PasswordResetRequestForm(forms.Form):
    correo = forms.EmailField(
        label="Correo electrónico",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Correo electrónico','autocomplete': 'off'})
    )
