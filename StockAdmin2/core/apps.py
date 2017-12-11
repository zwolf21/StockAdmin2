from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'


# core 앱의 역할
# - 다른 앱들이 공유 할수 있는 core 서비스, 모듈 제공
# - 서드 파티 앱들을 각 뷰에 적용 되도록 가공
# - models.py 에 다른 모델들 통합 -> 앱간 인터페이스
# - 되도록 결합도가 떨어지게(core 모듈이 없어도 동작에 지장 없도록) 만들것