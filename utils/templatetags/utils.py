from django import template
from pytils.numeral import choose_plural

register = template.Library()


@register.filter(name='add_class', is_safe=True)
def add_class(value, arg):
    """ Add CSS class to the HTML element. """
    css_classes = value.field.widget.attrs.get('class', '')
    if css_classes:
        css_classes += ' ' + arg
    else:
        css_classes = arg
    return value.as_widget(attrs={'class': css_classes})


@register.filter(name='format_price')
def format_price(value):
    """ Removes non-significant zeros. """
    return value.normalize() if value % 1 == 0 else value


@register.filter(name='get_attr')
def get_attr(attrs_dict, attr_name) -> str:
    """ Get an element attribute. """
    return attrs_dict.get(attr_name) or ''


@register.filter(name='ru_pluralize')
def ru_pluralize(value, variants):
    singular, plural1, plural2 = variants.split(',')
    value = int(value)
    return choose_plural(value, (singular, plural1, plural2))


@register.filter(name='has_tag')
def has_tag(messages, tag):
    return any(tag in message.tags for message in messages)
