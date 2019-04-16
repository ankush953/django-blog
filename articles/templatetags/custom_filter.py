from django import template

register = template.Library()

@register.filter(name='cut')
def cut(value,arg):
    '''
    This function removes all occurences of arg from val
    '''
    return value.replace(arg,'')