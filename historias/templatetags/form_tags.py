from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Añade/concatena clases CSS a un widget de formulario en templates.
    Uso:
        {{ form.mi_campo|add_class:"form-control" }}
    """
    try:
        # Si field es BoundField, usar as_widget con attrs
        return field.as_widget(attrs={"class": css_class})
    except Exception:
        # Fallback: devolver el field tal cual
        return field
