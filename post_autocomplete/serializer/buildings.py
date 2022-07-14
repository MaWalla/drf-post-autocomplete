from rest_framework import serializers


__all__ = ['SearchBuildingsSerializer']


class SearchBuildingsSerializer(serializers.Serializer):
    postal_code = serializers.CharField(max_length=10, required=False)
    city = serializers.CharField(max_length=128, required=False)
    district = serializers.CharField(max_length=128, required=False)
    street = serializers.CharField(max_length=128, required=False)
    house_number = serializers.CharField(max_length=128, required=False)
    distribution_code = serializers.CharField(max_length=128, required=False)
    combined = serializers.CharField(max_length=128, required=False)
