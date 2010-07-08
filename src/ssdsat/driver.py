import qrp.parsing
import sat.cnf

from cStringIO import StringIO
f = StringIO("v(x) :- q(x),r(x,X,y,Y)")

print qrp.parsing.parse(f)
