from tempfile import NamedTemporaryFile
from subprocess import Popen, PIPE
import os

import mcdsat.mcd
import options

# Possible SSDSAT targets

def mcd(views, queries, ontology, costs, preferences):
    # generate the MCD theory
    t = mcdsat.mcd.mcd_theory(queries[0], views)

    # feed the theory to the d-DNNF compiler
    nnf_filename = compile_ddnnf(t)

    # enumerate the models of the d-DNNF theory
    models = enumerate_models(nnf_filename)

    for m in models:
        print map(lambda v : t.vs.reverse(v), m)

# Supporting methods

def compile_ddnnf(theory):
    with NamedTemporaryFile(prefix="ssdsat.", suffix=".cnf") as cnf_file:
        theory.write_unweighted_cnf(cnf_file)
        cnf_file.seek(0)

        args = [options.c2d,
                "-in", cnf_file.name,
                "-smooth",
                "-reduce",
                "-dt_method", "4"]

        c2d_process = Popen(args, stdout = open(os.devnull, 'r'))
        c2d_process.wait()

        nnf_filename = "{0}.nnf".format(cnf_file.name)

    return nnf_filename

def enumerate_models(nnf_filename):
    """
    Enumerate the models of the d-DNNF theory specified at the given file and
    return them in a list. Each model is encoded as a list of the integer IDs
    of the variables made true in it.
    """

    args = [options.models,
            "--write-models",
            "--num", str(options.max_models),
            nnf_filename]

    models_process = Popen(args, stdout = PIPE)
    models_process.wait()

    models = models_process.stdout.readlines()

    #filter unneeded output
    for (i, e) in enumerate(models):
        if e.strip() == "--- models begin ---":
            begin = i + 1
            break

    for (i, e) in enumerate(reversed(models)):
        if e.strip() == "---- models end ----":
            end = len(models) - i - 1

    cleanup = lambda m : map(int, m.strip().strip("{}").split())
    return map(cleanup, models[begin:end])
