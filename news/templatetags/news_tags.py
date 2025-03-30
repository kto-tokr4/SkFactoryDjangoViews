from django import template


register = template.Library()

@register.filter()
def censor(value):
    if 'is' in value:
        return value.replace(' the ',' * ')
    else:
        return value
