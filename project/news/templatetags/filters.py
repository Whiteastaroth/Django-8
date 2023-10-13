import re
from django import template
from django.utils.safestring import mark_safe


register = template.Library()


BAD_WORDS = ['отказались', 'редиска', 'редиски', 'фуфло', 'кардан', 'кардана', 'бельмондо', 'заёб',
             'распиздяй', 'веблюдей', 'гунявый', 'гунявой', 'кака', 'кончитта', 'вомитнул', 'вомиторий',
             'обсерватория', 'пулька', 'сиська', 'трухлявый', 'туба', 'щайсе', 'пиздатый', 'пиздатом'
]

@register.filter(name='censorship')
def censor(text):
    for word in BAD_WORDS:
        pattern = re.compile(r'\b{}\b'.format(word), re.IGNORECASE)
        censored_word = word[0] + '*' * (len(word) - 1)
        text = re.sub(pattern, censored_word, text)
    return mark_safe(text)