
from jinja2 import Environment
from django.urls import reverse

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'url': lambda name, *args, **kwargs: reverse(name, args=args, kwargs=kwargs)
    })
    return env
