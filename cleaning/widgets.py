from django.contrib.admin.widgets import AdminFileWidget


class AdminImagePreviewWidget(AdminFileWidget):
    template_name = 'admin/widgets/image_preview.html'

