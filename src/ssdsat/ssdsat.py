from tempfile import NamedTemporaryFile
from subprocess import Popen, PIPE
import os
import logging

import mcdsat.mcd
import mcdsat.rw
import options
from qrp.views import View, Predicate

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

def rw(views, queries, ontology, costs, preferences):
    # generate the MCD theory
    t = mcdsat.mcd.mcd_theory(queries[0], views)

    # generate the RW theory based on the MCD theory
    rw_t = mcdsat.rw.rw_theory(queries[0], views, t)

    # feed the theory to the d-DNNF compiler
    nnf_filename = compile_ddnnf(rw_t)

    # enumerate the models of the d-DNNF theory
    models = enumerate_models(nnf_filename)

    for m in models:
        print rw_rebuild(queries[0], views, rw_t, m)

# Target-specific supporting methods

def rw_rebuild(query, views, theory, model):
    model_views = {}
    model_goals = {}
    model_mappings = {}

    for v in model:
        var = theory.vs.rev(v)
        copy = var[-1] # the last element marks the copy number
        kind = var[0]

        if kind == 'v':
            model_views[copy] = var[1]
        elif kind == 'g':
            model_goals[copy] = var[1]
        elif kind == 't':
            model_mappings.setdefault(copy, []).append((var[1], var[2]))

    goals = []
    newvar = 0

    for n in xrange(len(query.body)):
        args = []

        for arg in views[model_views[n]-1].head.arguments:
            appended = False

            for (x, y) in model_mappings[n]:
                if arg == y:
                    args.append(x)
                    appended = True
                    break

            if not appended:
                args.append("_" + str(newvar))
                newvar += 1

        goals.append(Predicate(views[model_views[n]-1].head.name, args))

    return View(query.head, goals)

# External tools

def compile_ddnnf(theory):
    """
    Returns the filename of the d-DNNF #TODO better to return file-like object?
    """

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

    logging.info("enumerating models")

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
