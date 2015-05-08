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
            output = linenums[line].current_best.output_file
            output.open()
            f.write(output.read())
            if line != len(graphs):
                f.write("\n")
            output.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Provide exactly one argument: python %s myoutputname.out" % __file__
    else:
        fname = sys.argv[1]
        main(fname)