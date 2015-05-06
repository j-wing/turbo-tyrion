import datetime

from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F
from django.http import Http404, HttpResponse
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count


from .utils import JSONResponse
from .models import InputGraph, Algorithm, GraphScore

def index(request):
    """
        Renders the current leaderboard of algorithms.
    """
    graphs = InputGraph.objects.all().order_by("-is_test_graph", "num_vars", "-current_best__path_cost")
    total_graphs = graphs.count()
    num_running = InputGraph.get_running().count()
    num_solved = InputGraph.objects.exclude(current_best=None).count()
    percent_solved = round(10000 * float(num_solved) / float(total_graphs)) / 100
    best_algos = Algorithm.objects.annotate(num_solved=Count("graphscore__graph__current_best")).order_by("-num_solved")[:3]
    return render(request, "index.html", {
        'graphs':graphs, 
        'num_running':num_running,
        'num_solved':num_solved,
        'best_algos':best_algos,
        'percent_solved':percent_solved,
        'total_graphs':total_graphs
        })

def claim_new_graphs(request):
    number = int(request.GET.get("number", 1))
    test_only = bool(request.GET.get("test_only", False))

    if test_only:
        ids = InputGraph.objects.filter(is_test_graph=True).order_by('num_vars')

    else:
        graphs = InputGraph.get_not_running().exclude(is_test_graph=True).filter(last_run_end=None).order_by(
            'num_vars', "-current_best__path_cost")[:number]
        ids = [g.pk for g in graphs]
        if len(graphs) < number:
            from_all = InputGraph.objects.exclude(id__in=ids).exclude(is_test_graph=True).order_by(
                    "-current_best__path_cost")[:(number - len(graphs))]

            ids.extend([g.pk for g in from_all])
        
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

@csrf_exempt
def add_result(request, graph_id):
    """
        Adds a score from the result of an algorithm.
    """
    if request.method != "POST":
        raise Http404, "Must add a result using POST"

    graph = get_object_or_404(InputGraph, pk=graph_id)
    post = request.POST
    valid, reason = graph.verify_solution(post['path'], post['path_cost'])
    if not valid:
        return JSONResponse({
            'success':False,
            'error':'Invalid path.',
            'code':1,
            'reason':reason
        })

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
    
    score = GraphScore(algo=algo, graph=graph, path_cost=int(post['path_cost']), path=post['path'], runtime=post['runtime'])
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

@csrf_exempt
def unclaim(request, graph_id):
    graph = get_object_or_404(InputGraph, pk=graph_id)
    # Reset these values so the graph will be claimed again.
    graph.last_run_end = None
    graph.last_run_start = None

    graph.save()
    return JSONResponse({'success':True})