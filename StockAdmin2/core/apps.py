from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'


# core 앱의 역할
# 1. 다른 앱들이 공유 할수 있는 서비스 제공
# 2. models.py 에 다른 모델들 통합 -> 앱간 인터페이스
