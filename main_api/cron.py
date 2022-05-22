from django.core import management
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings


def algolia_reindex_cron(request):
    # GCP App engine cron view
    # whitelist_ips = settings.ALGOLIA_REINDEX_WHITELIST_IPS
    # if request.META.get("HTTP_X_APPENGINE_CRON") and request.META.get('REMOTE_ADDR') and request.META.get("REMOTE_ADDR") in whitelist_ips:
    management.call_command('algolia_reindex', verbosity=0)
    management.call_command('admin_zone_algolia_reindex', verbosity=0)
    return HttpResponse('Algolia index refreshed')
    # else:
        # return HttpResponseForbidden("Forbidden")
