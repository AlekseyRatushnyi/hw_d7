from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
bad_words = ['редиска', 'картошка']


@register.filter
@stringfilter
def censor(value):
    for i in range(len(bad_words)):
        num_index = value.lower().find(bad_words[i])
        if num_index > 0:
            value = value.replace(bad_words[i][1:], "*" * (len(bad_words[i]) - 1))
    return value
