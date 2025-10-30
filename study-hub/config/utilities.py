# import git
# from config.settings import REPOSITORY_NAME
# from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def github_webhook(self, request):
    if request.method != "POST":
        return 0
    return 1
