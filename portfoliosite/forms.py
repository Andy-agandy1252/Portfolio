from django.contrib.auth.models import User
from .models import Report, UserProfile, Worker
from django.contrib.auth.forms import UserCreationForm
from django import forms
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderQuotaExceeded


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use. Please use a different email.")
        return email

class UserProfileForm(forms.ModelForm):
    city = forms.CharField(label='City', max_length=255, required=True, help_text='Required. Enter your city.')
    zipcode = forms.CharField(label='Zip Code', max_length=10, required=False)
    country = forms.CharField(label='Country', max_length=255, required=True)

    class Meta:
        model = UserProfile
        fields = ['city', 'zipcode', 'country']

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        zipcode = cleaned_data.get('zipcode')
        country = cleaned_data.get('country')

        # Perform geocoding to check if the location is valid
        geolocator = Nominatim(user_agent="your_geopy_app_name")

        if city:
            try:
                geocode_result = geolocator.geocode(city)
                if not geocode_result:
                    self.add_error('city', "Invalid city. Please enter a valid city.")
            except (GeocoderTimedOut, GeocoderQuotaExceeded):
                raise forms.ValidationError("Geocoding service error. Please try again later.")
            except Exception as e:
                raise forms.ValidationError(f"Geocoding error: {str(e)}")

        if zipcode:
            try:
                geocode_result = geolocator.geocode(zipcode)
                if not geocode_result:
                    self.add_error('zipcode', "Invalid zipcode. Please enter a valid zipcode.")
            except (GeocoderTimedOut, GeocoderQuotaExceeded):
                raise forms.ValidationError("Geocoding service error. Please try again later.")
            except Exception as e:
                raise forms.ValidationError(f"Geocoding error: {str(e)}")

        if country:
            try:
                geocode_result = geolocator.geocode(country)
                if not geocode_result:
                    self.add_error('country', "Invalid country. Please enter a valid country.")
            except (GeocoderTimedOut, GeocoderQuotaExceeded):
                raise forms.ValidationError("Geocoding service error. Please try again later.")
            except Exception as e:
                raise forms.ValidationError(f"Geocoding error: {str(e)}")

        return cleaned_data


class UserProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=150, required=True)
    email = forms.EmailField(label='Email', required=True)
    city = forms.CharField(label='City', max_length=255, required=True)
    zipcode = forms.CharField(label='Zip Code', max_length=10, required=False)
    country = forms.CharField(label='Country', max_length=255, required=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'city', 'zipcode', 'country']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        city = cleaned_data.get('city')
        zipcode = cleaned_data.get('zipcode')
        country = cleaned_data.get('country')

        # Perform geocoding to check if the location is valid
        geolocator = Nominatim(user_agent="your_geopy_app_name")

        if city:
            try:
                geocode_result = geolocator.geocode(city)
                if not geocode_result:
                    self.add_error('city', "Invalid city. Please enter a valid city.")
            except (GeocoderTimedOut, GeocoderQuotaExceeded):
                raise forms.ValidationError("Geocoding service error. Please try again later.")
            except Exception as e:
                raise forms.ValidationError(f"Geocoding error: {str(e)}")

        if zipcode:
            try:
                geocode_result = geolocator.geocode(zipcode)
                if not geocode_result:
                    self.add_error('zipcode', "Invalid zipcode. Please enter a valid zipcode.")
            except (GeocoderTimedOut, GeocoderQuotaExceeded):
                raise forms.ValidationError("Geocoding service error. Please try again later.")
            except Exception as e:
                raise forms.ValidationError(f"Geocoding error: {str(e)}")

        if country:
            try:
                geocode_result = geolocator.geocode(country)
                if not geocode_result:
                    self.add_error('country', "Invalid country. Please enter a valid country.")
            except (GeocoderTimedOut, GeocoderQuotaExceeded):
                raise forms.ValidationError("Geocoding service error. Please try again later.")
            except Exception as e:
                raise forms.ValidationError(f"Geocoding error: {str(e)}")

        return cleaned_data


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['street', 'house_number', 'city', 'zipcode', 'region', 'country', 'coordinates', 'garbage_image',
                  'street_image', 'commentary', 'status', 'issue_type']

    def clean_street_image(self):
        street_image = self.cleaned_data.get('street_image')

        # Check if the file extension is allowed for images
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
        if street_image:
            ext = street_image.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError('Invalid image format. Please use JPG, JPEG, PNG, or GIF.')

        return street_image


class GrantWorkerStatusForm(forms.Form):
    username = forms.CharField(label='Enter Username')

class RevokeWorkerStatusForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')


class ChangeStatusForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['class'] = 'form-control'


class WorkerStatusForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['status']


