from datetime import timedelta
from django import template


register = template.Library()


@register.filter
def format_time(value):
    if isinstance(value, str):
        hours, minutes, seconds = map(int, value.split(':'))
    elif isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
    else:
        return value  # or handle the error case appropriately

    result = []
    if hours > 0:
        result.append(f"{hours}h")
    if minutes > 0:
        result.append(f"{minutes}min")
    if hours == 0 and minutes == 0 and seconds > 0:
        result.append(f"{seconds}s")
    return ' '.join(result)
