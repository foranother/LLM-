from rest_framework import serializers


class FirebaseModelSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        return instance.save()
