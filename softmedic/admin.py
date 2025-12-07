from django.contrib import admin
from django.utils.html import format_html

# Personalización visual del panel de administración
admin.site.site_header = format_html(
    '<img src="/static/img/logo_softmedic.png" style="height:40px; margin-right:10px; vertical-align:middle;"> '
    '<span>SOFT-MEDIC - Administración</span>'
)
admin.site.index_title = "Panel principal"
admin.site.site_title = "SOFT-MEDIC Admin"
