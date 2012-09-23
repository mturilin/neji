# Create your views here.
import subprocess
import uuid
import django
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from neji.models import CodeSession
from django.conf import settings

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html', {"code": "print 'Hello, world!'", "session_id": ""})


def validate_python_code(python_code):
    if "import" in python_code:
        return ["Don't use imports!"]


def format_validation_errors(validation_errors):
    text = ''

    for error in validation_errors:
        text += " - %s\n" % error

    return text


@require_http_methods(["POST"])
def runpython(request):
    python_code = request.POST["python_code"]
    print "Python code=", python_code

    validation_errors = validate_python_code(python_code)

    if validation_errors:
        formatted_errors = format_validation_errors(validation_errors)

        return HttpResponse(simplejson.dumps({
            "output": '',
            "error": True,
            "error_message": "Errors:\n%s" % formatted_errors
        }))



    python_process = subprocess.Popen(["python"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        (output, error) = python_process.communicate(python_code)
    except Exception, e:
        logger.warning(e)
        raise e

    logger.debug("Output=" + output)
    logger.debug("Error=" + error)

    return_dict = {
        "output": output,
        "error": error != '',
        "error_message": error}

    return HttpResponse(simplejson.dumps(return_dict))


@require_http_methods(["POST"])
def new(request):
    python_code = request.POST["python_code"]
    new_uuid = uuid.uuid1().hex

    logger.debug("Creating new code session, uuid=" + new_uuid)

    code_session = CodeSession()
    code_session.session_id = new_uuid
    code_session.code = python_code

    code_session.save()

    return HttpResponse(reverse("session", args=[new_uuid]))


@require_http_methods(["POST"])
def save(request):
    python_code = request.POST["python_code"]
    session_id = request.POST["session_id"]

    logger.debug("Creating existing code session, uuid=" + session_id)

    code_session = get_object_or_404(CodeSession, session_id=session_id)
    code_session.code = python_code
    code_session.save()

    return HttpResponse("Okay! Saved!")


@ensure_csrf_cookie
def code_session_page(request, session_id):
    code_session = get_object_or_404(CodeSession, session_id=session_id)

    return render(request, 'index.html',
        {"code": code_session.code,
         "session_id": session_id,
         "ws_url": settings.WS_URL})

