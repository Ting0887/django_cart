from cartapp.models import User
from rest_framework import serializers,validators

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','email','phone')
        
        extra_kwargs = {
            "password":{"write_only":True},
            "email":{
                "required":True,
                "allow_blank":False,
                "validators":[
                    validators.UniqueValidator(User.objects.all())
                              ]
            }
        }
    def create(self,validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        phone = validated_data['phone']
        user = User.objects.create(
            username = username,
            password = password,
            email = email,
            phone = phone,
        )
        
        return user
        
        
        