import datetime

from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F
from django.http import Http404, HttpResponse
from django.core.files.base import ContentFile


from .utils import JSONResponse
from .models import InputGraph, Algorithm, GraphScore

def index(request):
    """
        Renders the current leaderboard of algorithms.
    """
    return render(request, "index.html", {'graphs':InputGraph.objects.all()})

def claim_new_graphs(request):
    number = int(request.GET.get("number", 1))
    test_only = bool(request.GET.get("test_only", False))

    if test_only:
        ids = InputGraph.objects.filter(is_test_graph=True).order_by('-current_best__path_cost')

    else:
        graphs = InputGraph.objects.filter(
                                    Q(last_run_start=None) | Q(last_run_start__gt=F("last_run_end"))).order_by(
                                    "-current_best__path_cost")[:number]
        ids = [g.pk for g in graphs]
        if len(graphs) < number:
            graphs.extend(InputGraph.objects.exclude(id__in=ids).order_by("-current_best__path_cost")[:(number - len(graphs))])
            ids = [g.pk for g in graphs]
        
        InputGraph.objects.filter(pk__in=ids).update(last_run_start=datetime.datetime.now())
    return JSONResponse({'success':True, 'graph_ids':ids})

def get_graph(request, graph_id):
    """
        Returns the contents of a graph's .in file.
    """
    graph = get_object_or_404(InputGraph, pk=graph_id)
    with open(graph.get_input_abspath(), 'r') as f:
        resp = HttpResponse(f.read(), content_type="text/plain")
    return resp

def add_result(request, graph_id):
    """
        Adds a score from the result of an algorithm.
    """
    # if request.method != "POST":
    #     raise Http404, "Must add a result using POST"

    graph = get_object_or_404(InputGraph, pk=graph_id)
    post = request.GET

    if post.get('algorithm_id'):
        algo = Algorithm.objects.get(pk=post['algorithm_id'])
    else:
        try:
            algo = Algorithm.objects.get(command=post['algorithm_command'])
            if algo.name != post['algorithm_name']:
                algo.name = post['algorithm_name']
                algo.save()
        except Algorithm.DoesNotExist:
            algo = Algorithm(name=post['algorithm_name'], command=post['algorithm_command'])
            algo.save()
    
    score = GraphScore(algo=algo, graph=graph, path_cost=int(post['path_cost']), path=post['path'])
    score.output_file.save("", ContentFile(post['out']))
    score.save()

    new_leader = False
    current_best = None if graph.current_best is None else graph.current_best.path_cost
    if current_best is None or score.path_cost < current_best:
        graph.current_best = score
        new_leader = True
    graph.last_run_end = datetime.datetime.now()
    graph.save()

    return JSONResponse({
        'success':True, 
        'score_id':score.pk, 
        'graph_id':graph.pk, 
        'algo_id':algo.pk, 
        'new_leader':new_leader,
        'lead_score':current_best
    })