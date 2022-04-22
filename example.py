import itertools
from lib import algorithm
from sympy import *
from pathlib import Path
from operator import mul
from math import factorial
from functools import reduce
import sys
init_printing(use_unicode=False)

def sum_checker(M):
    def f(v):
        return (sum(v) < M)
    return f


def check_all_states(N, M, f):
    return [v for v in itertools.product(range(M), repeat=N) if f(v)]


def states_for_phase_execution(N, M):
    return check_all_states(N, M, sum_checker(M))


def create_my_numerate(M):
    def my_norm(x):
        return sum([k*M**i for i, k in enumerate(x)])
    return my_norm


def get_list_of_states(N, M): 
    return sorted(states_for_phase_execution(N, M+1),
        key=create_my_numerate(M+1))


def create_ordinar_difference_of_vector(N):
    def f(z, y):
        i_minus = N
        i_plus = N
        for i, (m, k) in enumerate(zip(z, y)):
            diff = m - k
            if abs(diff) > 1:
                return (N, N), False
            if diff == 1:
                if i_plus == N:
                    i_plus = i
                else:
                    return (N, N), False
            if diff == -1:
                if i_minus == N:
                    i_minus = i
                else:
                    return (N, N), False
        return (i_minus, i_plus), True
    return f


def create_phase_execution_local_arg_maker(N):
    diff_f = create_ordinar_difference_of_vector(N)

    def create_local_arg(q, y, z, const_arg):
        (i_minus, i_plus), check = diff_f(z, y)
        no_minus = (i_minus == N)
        no_plus = (i_plus == N)
        is_minus = not no_minus
        is_plus = not no_plus
        no_change = (q == 0)
        plus_change = (q == 1)
        minus_change = (q == -1)
        arg = {'i_minus': i_minus, 'i_plus': i_plus,
               'no_minus': no_minus, 'no_plus': no_plus,
               'is_minus': is_minus, 'is_plus': is_plus,
               'check': check, 'no_change': no_change,
               'plus_change': plus_change,
               'minus_change': minus_change}
        return arg

    return create_local_arg


def create_phase_execution_LFL(M):
    def poiss_checker(q, y, z, const_arg, arg):
        right_state_change = arg['no_minus'] and arg['is_plus']
        return arg['check'] and arg['no_change'] and right_state_change

    def poiss(q, y, z, const_arg, arg):
        qk = const_arg['q'][arg['i_plus']]
        lam = const_arg['lam']
        return lam*qk

    def out_orbit_checker(q, y, z, const_arg, arg):
        right_state_change = arg['no_minus'] and arg['is_plus']
        return arg['check'] and arg['minus_change'] and right_state_change

    def out_orbit(q, y, z, const_arg, arg):
        return 0

    def out_orbit_(q, y, z, const_arg, arg):
        qk = const_arg['q'][arg['i_plus']]
        sigma = const_arg['sigma']
        return sigma*qk

    def in_orbit_checker(q, y, z, const_arg, arg):
        right_state_change = arg['is_minus'] and arg['no_plus']
        return arg['check'] and arg['plus_change'] and right_state_change

    def in_orbit(q, y, z, const_arg, arg):
        k = arg['i_minus']
        uk = const_arg['u'][k]
        r2 = const_arg['r2']
        return y[k]*uk*r2

    def in_orbit_full_checker(q, y, z, const_arg, arg):
        right_state = arg['no_minus'] and arg['no_plus'] and (sum(y) == M)
        return arg['check'] and arg['plus_change'] and right_state

    def in_orbit_full(q, y, z, const_arg, arg):
        return const_arg['lam']

    def exit_checker(q, y, z, const_arg, arg):
        right_state_change = arg['is_minus'] and arg['no_plus']
        return arg['check'] and arg['no_change'] and right_state_change

    def exit_zero(q, y, z, arg_dict, temp_arg_dict):
        k = temp_arg_dict['i_minus']
        uk = arg_dict['u'][k]
        r0 = arg_dict['r0']
        return y[k]*uk*r0

    def again_checker(q, y, z, const_arg, arg):
        right_state_change = arg['is_minus'] and arg['is_plus']
        return arg['check'] and arg['no_change'] and right_state_change

    def again(q, y, z, const_arg, arg):
        k = arg['i_minus']
        uk = const_arg['u'][k]
        r1 = const_arg['r1']
        return y[k]*uk*r1*const_arg['q'][arg['i_plus']]

    return [[poiss_checker, poiss], [out_orbit_checker, out_orbit, out_orbit_],
            [exit_checker, exit_zero], [in_orbit_full_checker, in_orbit_full],
            [in_orbit_checker, in_orbit], [again_checker, again]]


def get_all_math_variables(N):
    u = symbols('u0:{}'.format(N))
    _q = symbols('q0:{}'.format(N-1))
    q = tuple(list(_q) + [1 - sum(_q)])
    lam, sigma, r0, r2 = symbols('lam sigma r0 r2')
    math_variables = {
        'u': u, 'q': q, 'lam': lam, 'sigma': sigma,
        'r0': r0, 'r1': (1 - r0 - r2), 'r2': r2}
    return math_variables

def solve_phase_execution(state_list, const_arg, LFL, local_arg_maker):
    return algorithm(state_list, 1, 1, const_arg, LFL, local_arg_maker)

def unique_of_r(n, q, u):
    return (q/u)**n/factorial(n)

def product_of_unique_of_r(nv, var):
    return reduce(mul, 
        [unique_of_r(n, q, u) for n, q, u 
            in zip(nv, var["q"], var["u"])], 1) 

def unity_of_r(x, var):
    return (var["lam"]+x)/(1-var["r1"])

def get_element_of_r_from_n_vector(x, nv, var):
    return unity_of_r(x, var)**sum(nv)*product_of_unique_of_r(nv, var) 

def get_r(x, state_list, var):
    return Matrix([[get_element_of_r_from_n_vector(x, n, var)
        for n in state_list]])

"""
def save_tables_in_directory(tables, dir_path):
    p = Path(dir_path)
    p.mkdir(parents=True, exist_ok=True)
    for n, M in enumerate(tables[0]):
        with open(p / ('_{}.txt'.format(n)), 'w') as f:
            f.write(pretty(M, wrap_line =False).replace('[', '').replace(']', ''))
    for q, lst in enumerate(tables[1:]):
        for n, M in enumerate(lst):
            with open(p / ('{}_{}.txt'.format(q, n)), 'w') as f:
                f.write(pretty(M, wrap_line =False).replace('[', '').replace(']', ''))
"""

def get_D(*lst):
    #print([M*ones(shape(M)[1],1) for M in lst])
    return diag(
        *sum([M*ones(shape(M)[1],1) for M in lst], 
            zeros(shape(lst[0])[1],1)))

def get_S_from_scheme(x, tables, var):
    A = tables[1][0] - get_D(tables[1][0], tables[2][0])
    B = tables[2][0]
    K = tables[0][1]/var["sigma"]
    I = get_D(K)
    return (A+B + x*(K - I)) 

def is_r_to_S_zero(r, S):
    return (simplify(r*S) == zeros(*shape(r)))

def is_formula_right(m, n):
    var = get_all_math_variables(n)
    states = get_list_of_states(n, m)
    LFL = create_phase_execution_LFL(n)
    local = create_phase_execution_local_arg_maker(n)    
    scheme = solve_phase_execution(states, var, LFL, local)
    x = symbols("x")
    r = get_r(x, states, var)
    S = get_S_from_scheme(x, scheme, var)
    return is_r_to_S_zero(r,S)

def main(m, n):
    for i in m:
        for j in n:
            print(is_formula_right(i,j))

if __name__ == "__main__":
    main(
        range(int(sys.argv[1]), int(sys.argv[2])),
        range(int(sys.argv[3]), int(sys.argv[4])))