from sympy import *
from m_phase_n_execution import m_phase_n_execution_get_ABKI
M = 1
N = 1 
us = symbols('u0:{}'.format(M))
_qs = symbols('q0:{}'.format(M-1))
qs = tuple(list(_qs) + [1 - sum(_qs)])
lam, r0, r2 = symbols('lam r0 r2')
print(m_phase_n_execution_get_ABKI(M, N, lam, r0, r2, qs, us), sep="\n")
