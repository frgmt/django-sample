def get_client_ip(request):
    """Parses a request META 'HTTP_X_FORWARDED_FOR' and return client ip string

    See http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    """
    # if behind the ELB.
    # HTTP_X_FORWARDED_FOR: client, proxy1, proxy2...
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded:
        client_ip = x_forwarded.split(',')[0].strip()
    else:
        client_ip = request.META.get('REMOTE_ADDR').strip()

    return client_ip


def set_api_version_prematurely(view):
    """ used primarily from view's get_permissions() since versioning will be processed after check_permissions() call
     in view.initial().
    :param view: view object
    :return: None
    """
    # Perform content negotiation and store the accepted info on the request
    neg = view.perform_content_negotiation(view.request)
    view.request.accepted_renderer, view.request.accepted_media_type = neg

    # Determine the API version, if versioning is in use.
    version, scheme = view.determine_version(view.request, *view.args, **view.kwargs)
    view.request.version, view.request.versioning_scheme = version, scheme


def get_item_from_request(request, key):
    """ acts just like request.REQUEST which is deprecated as of Django 1.7.
    :param request: request
    :param key: string dict's key
    :return: value
    """
    assert request and key
    value = request.POST.get(key)
    if value is None:
        value = request.GET.get(key)
    return value
