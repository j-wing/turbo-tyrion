import os
from django.db import models
from django.conf import settings

PATH_MAX_LEN = 255

def get_path(relpath):
    """
        Returns the absolute path to a directory relative to the current directory.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relpath))

class Algorithm(models.Model):
    name = models.CharField(max_length=255)
    command = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class GraphScore(models.Model):
    algo = models.ForeignKey(Algorithm)
    path_cost = models.IntegerField()
    path = models.TextField()
    graph = models.ForeignKey('InputGraph')
    output_filename = models.FilePathField(max_length=PATH_MAX_LEN, path=get_path("outputs"))

    def __unicode__(self):
        return "Score of %s on %s" % (path_cost, graph)


class InputGraph(models.Model):
    input_filename = models.FilePathField(max_length=PATH_MAX_LEN, path=get_path("inputs"))
    current_best = models.ForeignKey(GraphScore, null=True, blank=True)
    last_run_start = models.DateTimeField(null=True, blank=True)
    last_run_end = models.DateTimeField(null=True, blank=True)
    is_test_graph = models.BooleanField(default=False)

    def __unicode__(self):
        return self.input_filename

    def is_running(self):
        return (self.last_run_start and self.last_run_end is None) or (self.last_run_start > self.last_run_end) \
                or (self.last_run_end - self.last_run_start > settings.GRAPH_CLAIM_EXPIRATION)

    def get_input_abspath(self):
        return os.path.join(get_path("inputs"), self.input_filename)