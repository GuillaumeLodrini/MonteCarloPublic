import os
import json

from django.http import HttpResponse, HttpResponseForbidden
from celery import Celery
from celery.result import AsyncResult
from decimal import Decimal


"""
Exemple of task (to put in tasks.py):
------------------------------------

# xxx/task.py
@app.task(bind=True)
def custom_task(self, elts, download_csv=False):
 def custom_task_filename(f_elts):
     # Prepare file path + Create directory
     filename = "myfile.csv"
     path = os.path.join(settings.MEDIA_ROOT, 'celery', filename)
     dirname = os.path.dirname(path)
     if not os.path.exists(dirname):
         os.makedirs(dirname)
     # Generate CSV file
     with open(path, "w") as f:
         writer = csv.writer(f, quoting=csv.QUOTE_ALL)
         for elt in f_elts:
             writer.writerow([elt])
     return path

 errors = []
 # Init progress bar
 progress_recorder = ProgressRecorder(self)
 progress_len = len(elts)
 for i, elt in enumerate(elts):
     try:
       [...]
     except:
       errors.append("my custom error")
     # increment progess bar
     progress_recorder.set_progress(i, progress_len)
 # Finish task with errors informations
 if len(errors) > 0:
     return {'errors': errors}
 # Finish task with filename informations
 if download_csv:
     return {'filename': custom_task_filename(elts)}

# xxx/views.py
# Run celery tasks
result = xxx.tasks.custom_task.delay(elts, download_csv)
return render(
    self.request,
    'celery_progress.html',
    context=dict(
        task_id=result.task_id,
        title='PROGRESSBAR TITLE',
        message='PROGRESSBAR LOADING MESSAGE',
        success_message="PROGRESSBAR SUCCESS MESSAGE",
        error_message="PROGRESSBAR ERROR MESSAGE",
        next_url=reverse_lazy('custom_url')
     ))
"""

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MonteCarlo.settings')
app = Celery('MonteCarlo')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


class ProgressRecorder(object):
    """
    Celery ProgressRecorder
    These object is use to recording progress tasks values
    """

    def __init__(self, task):
        self.task = task

    # Set current progress
    def set_progress(self, current, total):
        percent = round((Decimal(current) / Decimal(total)) * Decimal(100), 2) if total > 0 else 0
        self.task.update_state(
            state='PROGRESS',
            meta={
                'current': current,
                'total': total,
                'percent': percent
            }
        )


class Progress(object):
    """
    Celery Progress
    These object is use to return specific task progress
    """

    def __init__(self, task_id):
        self.task_id = task_id
        self.result = AsyncResult(str(task_id))

    def get_info(self):
        # if task is finish
        if self.result.ready():
            # Get task result
            result = self.result.get()
            # Get errors / filename informations
            errors = result.get('errors', None) if result else None
            filename = result.get('filename', None) if result else None
            # CUSTOM FAILURE
            if errors:
                return {
                    'complete': True,
                    'success': False,
                    'progress': {
                        'current': 100,
                        'total': 100,
                        'percent': 100,
                    },
                    'errors': errors
                }
            # CUSTOM SUCCESS WITH FILE DOWNLOAD
            if filename:
                return {
                    'complete': True,
                    'success': True,
                    'progress': {
                        'current': 100,
                        'total': 100,
                        'percent': 100,
                    },
                    'filename': filename
                }
            # SUCCESS/FAILURE
            return {
                'complete': True,
                'success': self.result.successful(),
                'progress': {
                    'current': 100,
                    'total': 100,
                    'percent': 100,
                }
            }
        elif self.result.state == 'PROGRESS':
            return {
                'complete': False,
                'success': None,
                'progress': self.result.info  # Get informations stored by ProgressRecorder.set_progress method. (cf. meta field)
            }
        elif self.result.state in ['PENDING', 'STARTED']:
            return {
                'complete': False,
                'success': None,
                'progress': {
                    'current': 0,
                    'total': 100,
                    'percent': 0,
                }
            }
        return self.result.info


# Celery Function Views
# Theses views are automatically called into templates/celery_progress.html file

def celery_progress(request, task_id):
    """ Function views of /celery_progress/<TASK_ID> url """

    # Return current task progression
    progress = Progress(task_id)
    return HttpResponse(json.dumps(progress.get_info()), content_type='application/json')


def celery_download(request, task_id):
    """ Function views of /celery_progress/<TASK_ID> url """

    # Return generated CSV file
    result = AsyncResult(str(task_id))
    # Get task filename informations
    filename = result.get().get('filename', None) if result else None
    # if task is finish and get filename informations
    if result.ready() and filename:
        try:
            f = open(filename, mode='rb')
        except:
            return HttpResponseForbidden()
        else:
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' if '.xlsx' in filename else 'text/csv'
            response = HttpResponse(f, content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename=%s' % filename.split('/')[-1]
        return response
    return HttpResponseForbidden()
