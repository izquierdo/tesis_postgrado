import qrp.parsing
import sat.cnf

print qrp.parsing.pepe("v(x) :- q(x),r(x,X,y,Y)")
