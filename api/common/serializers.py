from rest_framework import serializers

class GroupBySerializer(serializers.Serializer):
    key = serializers.CharField(max_length=100)
    count = serializers.IntegerField()
    items =serializers.CharField(allow_null=True)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in instance.items():
            if key not in ["key", "count", "items"]:
                data[key] = value
        return data