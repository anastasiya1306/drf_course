from rest_framework import serializers


class VideoValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value.get('link_video'):
            if 'www.youtube.com' not in value.get('link_video'):
                raise serializers.ValidationError('Запрещены ссылки на сторонние ресурсы, кроме youtube.com')
