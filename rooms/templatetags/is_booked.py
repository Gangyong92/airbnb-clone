import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()

# takes_context=True: django가 전달해 주는 user나 다른 context를 받을 수 있음.
# 근데 여기서 적용은 안함.
@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return
    try:
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        # 있는지 없는지 확인용임. 없으면 except로 갈거임.
        reservation_models.BookedDay.objects.get(day=date, reservation__room=room)
        return True
    except reservation_models.BookedDay.DoesNotExist:
        return False
