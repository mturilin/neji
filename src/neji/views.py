# Create your views here.
import subprocess
from threading import Timer
import uuid
import django
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
import re
from neji.models import CodeSession
from django.conf import settings

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html', {"code": "print 'Hello, world!'", "session_id": ""})


ALLOWED_PACKAGES = [
    "string",
    "re",
    "struct",
    "datetime",
    "numbers",
    "math",
    "decimal",
    "fractions",
    "random",
    "itertools",
    "functool",
    "operator",
    "pickle",
    "cPickle",
    "zlib",
    "gzip",
    "bz2",
    "zipfile",
    "csv",
    "io",
    "time",
    "threading",
    "time",
    "json",
]


def validate_python_code(python_code):
    import_errors = []
    REXP = "([import|from]\\s+(\\w+))\\W"
    for match in re.finditer(REXP, python_code):
        module_name = match.group(2)
        if module_name not in ALLOWED_PACKAGES:
            import_errors.append('Import from module "%s" is not allowed. Check Python page for explanation.' % module_name)

    return import_errors

def format_validation_errors(validation_errors):
    text = ''

    for error in validation_errors:
        text += " - %s\n" % error

    return text


TIMER_WAIT = 3.0

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

    # Timer
    timer_error = list()
    def check_and_kill():
        print "Before polling"
        process_poll = python_process.poll()
        print "Process poll= %s" % process_poll
        if process_poll is None:
            logger.info("Process terminated by timer")
            python_process.terminate()
            timer_error.append("Process was termitated by timeout because it took more than %d second" % TIMER_WAIT)


    timer = Timer(TIMER_WAIT, check_and_kill)
    timer.start()

    try:
        (output, error) = python_process.communicate(python_code)
    except Exception, e:
        logger.warning(e)
        raise e

    if timer_error:
        error = timer_error[0]

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

