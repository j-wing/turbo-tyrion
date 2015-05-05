import os, shutil, sys, argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.environ['DJANGO_SETTINGS_MODULE'] = 'nptsp_leaders.settings'
import django
django.setup()
from main.models import InputGraph, get_path

def main(dir, is_test=False):
    names = os.listdir(dir)
    added = []
    for name in names:
        path = os.path.join(dir, name)
        print "Testing", path
        if not InputGraph.objects.filter(input_filename=name, is_test_graph=is_test).count():
            target = os.path.join(get_path("inputs"), name)
            print "Moving input file from %s to %s..." % (path, target)
            shutil.copyfile(path, target)
            print "Creating new input graph..."
            g = InputGraph.objects.create(input_filename=name, is_test_graph=is_test)
            added = g
    print "Done. "
    print "Created %s new objects: " % len(added)
    print added

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Imports all unexisting test files from `dir`.')
    parser.add_argument('dir', type=str, help='directory to import from')
    parser.add_argument('--test', dest='test', action='store_true',
                       help='import as a test graph')

    args = parser.parse_args()
    main(args.dir, args.test)
