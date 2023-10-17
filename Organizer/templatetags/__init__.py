from django import template
from Organizer.templatetags.custom_filters import get_item

register = template.Library()

register.filter('get_item', get_item)