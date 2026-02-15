from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer): #ModelSerializer creates serializers based on your model
    # this class handles user data (Me)
    class Meta:
        model = CustomUser

        # which fields are going to be included in the JSON output
        fields = ['id', 'username', 'email', 'phone_number', 'date_joined']

        #cannot be changed
        read_only_fields = ['id', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    # this class handles user registration
    # we need to accept password (but never return it)
    # confirm password matches
    # hash the password before saving
    class Meta:
        model = CustomUser

        # password2 is an extra field that will be digarded before the data is saved to db
        fields = ['username', 'email', 'password', 'password2', 'phone_number']

        # extra_kwargs fine tunes specific fields (inheriting)
        extra_kwargs = {
            'email': {
                'required': True,
                'help_text': 'Will be used for login'
            },
            'username': {
                'help_text': 'Required. Name that can be identified by other players is recommended.'
            }
        }

        def validate(self, data):
            # runs a field level validation
            # data is a dictionary containing all submited fields
            password = data.get('password')
            password2 = data.get('password2')

            if password != password2:

                # raise a validation error
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match"}
                )

            return data

        def create(self, validated_data):
            # validated_data is the cleaned data after all validation passes
            # password2 needs to be removed

            validated_data.pop('password2')

            # **validated_data: ** is the dictionary unpacking op
            user = CustomUser.objects.create_user(**validated_data)

            return user


class LoginSerializers(serializers.Serializer):
    # accept email/password and validate them

    email = serializers.EmailField(
        write_only=True,
        help_text="Your registered email address"
    )

    password = serializers.CharField(
        write_only=True, # only accept, never return
        style={'input_type': 'password'}, # ••• instead of 123
        help_text = 'Your password'
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # make sure both are provided
        if not email or not password:
            raise serializers.ValidationError(
                "Both email and password are required."
            )

        # use django's authentication funct
        # username is expected as a parameter but USERNAME_FIELD was set to email
        user = authenticate(
            request=self.context.get('request'), # A request from the user (HTTP)
            username=email, # should be username=username but email is used instead
            password=password
        )

        #if not user was returned
        if not user:
            raise serializers.ValidationError(
                "Unable to log in with provided credentials."
            )

        #otherwise
        data['user'] = user #passes user data to a template for rendering
        return data