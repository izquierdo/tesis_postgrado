from tempfile import NamedTemporaryFile
from subprocess import Popen

from mcdsat import mcd

def compile_ddnnf(theory):
    with NamedTemporaryFile(prefix="ssdsat.", suffix=".cnf") as cnf_file:
        theory.write_unweighted_cnf(cnf_file)
        cnf_file.seek(0)

        args = [""
        Popen



def mcd(views, queries, ontology, costs, preferences):
    # generate the MCD theory
    t = mcd.mcd_theory(query, views)

    # feed the theory to the d-DNNF compiler
    compile_ddnnf(t)
