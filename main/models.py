import os, time
from django.db import models
from django.conf import settings
from django.db.models import Q, F

from tsp.util import *

PATH_MAX_LEN = 255

def get_path(relpath):
    """
        Returns the absolute path to a directory relative to the current directory.
    """
    return os.path.join(settings.MEDIA_ROOT, relpath)

def get_output_name(instance, filename):
    return "outputs/%s_%s.out" % (int(time.time()), instance.algo.pk)

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
    output_file = models.FileField(upload_to=get_output_name, null=True, blank=True)
    runtime = models.IntegerField()

    def __unicode__(self):
        return "Score of %s on %s" % (self.path_cost, self.graph)


class InputGraph(models.Model):
    input_filename = models.FilePathField(max_length=PATH_MAX_LEN, path=get_path("inputs"))
    current_best = models.ForeignKey(GraphScore, null=True, blank=True)
    last_run_start = models.DateTimeField(null=True, blank=True)
    last_run_end = models.DateTimeField(null=True, blank=True)
    is_test_graph = models.BooleanField(default=False)
    num_vars = models.IntegerField()

    def __unicode__(self):
        return self.input_filename

    @staticmethod
    def get_not_running_Q():
        return Q(last_run_start=None) | Q(last_run_end__gt=F("last_run_start"))

    @classmethod
    def get_running(cls):
        return cls.objects.exclude(cls.get_not_running_Q())

    @classmethod
    def get_not_running(cls):
        return cls.objects.filter(cls.get_not_running_Q())

    def is_running(self):
        if self.last_run_start is None:
            return False
        return (self.last_run_start and self.last_run_end is None) or (self.last_run_start > self.last_run_end) \
                or (self.last_run_end - self.last_run_start > settings.GRAPH_CLAIM_EXPIRATION)

    def get_input_abspath(self):
        return os.path.join(get_path("inputs"), self.input_filename)

    def verify_solution(self, path, est_cost):
        """
            Verifies that path specified by `path` is a valid path, and its cost matches est_cost.
        """

        graph = extract_input(os.path.join(get_path("inputs"), self.input_filename))

        path_nodes = path.split(" ")
        cost = 0
        reason = None

        if len(path_nodes) != self.num_vars:
            reason = 'Number of nodes in path doesn\'t match the number of vertices in the graph.' 
            return False, reason

        if '0' not in path_nodes:
            path_nodes = [int(n)-1 for n in path_nodes]
        else:
            path_nodes = [int(n) for n in path_nodes]

        last_colors = (None, None, None)
        for i in range(len(path_nodes) - 1):
            current_node = path_nodes[i]
            edge_cost = get_weight(get_edge(graph, current_node, path_nodes[i+1]))
            cost += edge_cost

            # Verify the color constraint
            curr_color = get_color(graph, current_node)
            if last_colors.count(curr_color) == 3:
                reason = "4 %s in a row: %s %s %s %s" % (curr_color, path_nodes[i-3], path_nodes[i-2], path_nodes[i-1], current_node)
                return False, reason
            else:
                last_colors = last_colors[1:] + (curr_color,)

        if last_colors.count(get_color(graph, path_nodes[-1])) == 3:
            reason = 'Last 4 nodes have same color.'
            return False, reason

        if est_cost != cost:
            reason = 'Cost is incorrect: actual=%s, yours=%s' % (cost, est_cost)
            return False, reason
        return True,''

