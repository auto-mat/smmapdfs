from .email import get_base_url, send_pdfsandwichs_from_queryset

def pdfsandwich_actions(sandwich_model):
    def make_pdfsandwich(modeladmin, request, queryset):
        for obj in queryset:
            sandwich, _ = sandwich_model.sandwich_model.objects.get_or_create(
                obj=obj,
                pdfsandwich_type=sandwich_model.get_sandwich_type(obj),
                )
            sandwich.update_pdf(obj, sandwich_model.sandwich_field_model)
            sandwich.save()

    return (make_pdfsandwich,)

def send_pdfsandwich(modeladmin, request, queryset):
    send_pdfsandwichs_from_queryset(queryset, get_base_url(request, ""))
