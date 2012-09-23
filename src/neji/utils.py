__author__ = 'mturilin'


def current_url(request):
    return {'current_url': "http://" + request.get_host() + request.get_full_path()}