from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from orders.models import Order


@method_decorator(staff_member_required, name='dispatch')
class AdminOrderDetailView(DetailView):
    """
    Display detailed information about the order.
    Available only to site staff.

    Attributes:
        model (Order): The model used in the view (Order Model);
        template_name (str): Path to the template the view renders;
        context_object_name (str): A variable name to use in context;
        pk_url_kwarg (str): URLConf keyword argument that contains the primary key.
    """
    model: Order = Order
    template_name: str = 'admin/orders/order/detail.html'
    context_object_name: str = 'order'
    pk_url_kwarg: str = 'order_id'
