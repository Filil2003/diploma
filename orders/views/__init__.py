"""
The 'views' package contains views for handling 'orders' views.

The following submodules included:
    - 'admin_order_detail_view': Contains a view for processing
        detailed information about the order in the admin panel;
    - 'order_create_wizard_view': Contains a wizard view for processing checkout.
"""

from .admin_order_detail_view import AdminOrderDetailView
from .order_create_wizard_view import OrderCreateWizardView
