from django.shortcuts import render


def bad_request_view(request, exception):
    return render(request, 'exceptions/400.html', status=400, context={
        'title': 'Bad Request',
        'error_message': 'Bad Request'
    })


def permission_denied_view(request, exception):
    return render(request, 'exceptions/403.html', status=403, context={
        'title': 'Permission Denied',
        'error_message': 'Permission Denied'
    })


def page_not_found_view(request, exception):
    for key, value in exception.messages.items():
        print(key, value)
    return render(request, 'exceptions/404.html', status=404, context={
        'title': 'Page Not Found',
        'error_message': 'Page Not Found'
    })


def server_error_view(request):
    return render(request, 'exceptions/500.html', status=500, context={
        'title': 'Server Error',
        'error_message': 'Internal Server Error'
    })
