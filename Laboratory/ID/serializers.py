from rest_framework import serializers
from .models import Request, SharedDetails

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
    def validate(self, data):
        # Check if the company name is provided
        if 'company_name' not in data:
            raise serializers.ValidationError("Company name is required.")

        # Check if requested details are provided
        if 'requested_details' not in data:
            raise serializers.ValidationError("Requested details are required.")

        # Check if only valid details are requested
        valid_details = {'name', 'phone', 'age', 'sex', 'caste', 'address', 'marital_status'}
        requested_details = set(data['requested_details'].split(','))
        invalid_details = requested_details - valid_details
        if invalid_details:
            raise serializers.ValidationError(f"Invalid details requested: {', '.join(invalid_details)}")

        return data

class SharedDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedDetails
        fields = '__all__'
