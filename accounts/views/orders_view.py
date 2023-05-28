from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from orders.models import Order


class OrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'accounts/orders.html'
    context_object_name = 'orders'
    paginate_by = 2
    extra_context = {
        'title': 'Мои уборки'
    }

    def get_queryset(self):
        status = self.request.GET.get('status')
        user = self.request.user
        queryset = super().get_queryset()
        if status == 'completed':
            execution_status = Order.ExecutionStatusEnum.COMPLETED
        else:
            execution_status = Order.ExecutionStatusEnum.CREATED
        queryset = queryset.filter(
            customer=user,
            execution_status=execution_status
        ).order_by('scheduled_date', 'scheduled_time')
        return queryset
