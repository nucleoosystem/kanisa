from django import template
from kanisa.utils.branding import BrandingInformation


register = template.Library()


@register.assignment_tag
def kanisa_branding(branding_component):
    try:
        brand = BrandingInformation(branding_component)
    except ValueError:
        return None

    return brand
