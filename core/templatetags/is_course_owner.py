from django import template
register = template.Library()

@register.filter(name='is_course_owner')
def is_course_owner(user, course):
    return user.pk == course.user_id