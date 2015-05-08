#!/usr/bin/env python
import os, shutil, sys, argparse, time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ['DJANGO_SETTINGS_MODULE'] = 'nptsp_leaders.settings'
import django
django.setup()

from main.models import InputGraph

def main(fname):
    graphs = InputGraph.objects.exclude(is_test_graph=True).order_by("input_filename")
    linenums = {}
    for graph in graphs:
        input_id = int(graph.input_filename.split(".")[0])
        linenums[input_id] = graph

    with open(fname, "w") as f:
        for line in range(1, len(graphs)+1):
            contents = get_contents(linenums, line)

            f.write(contents)
            if line != len(graphs):
                f.write("\n")

    print "Wrote to", fname
    print "Verifying contents..."

    with open(fname, "r") as f:
        had_error = False
        for i, line in enumerate(f, 1):
            graph = linenums[i]

            contents = get_contents(linenums, i)
            if contents != line:
                had_error = True
                print_badness(i, line, contents, "")

            valid, reason = graph.verify_solution(line, graph.current_best.path_cost)
            if not valid:
                print_badness(i, line, contents, reason)
                had_error = True
        if not had_error:
            print "Success!"


def get_contents(linenums, line):
    output = linenums[line].current_best.output_file
    output.open()
    contents = output.read()
    try:
        l = eval(contents)
    except SyntaxError:
        pass
    else:
        contents = " ".join((str(x) for x in l))
    output.close()
    return contents


def print_badness(lineno, line, contents, reason):
        print "INVALID: line no.", lineno
        print "In answer.out:", line
        print "In graph:", contents
        print "Reason was:", reason


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Provide exactly one argument: python %s myoutputname.out" % __file__
    else:
        fname = sys.argv[1]
        main(fname)