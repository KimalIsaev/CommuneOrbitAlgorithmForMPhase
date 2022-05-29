import itertools
from sympy import *


def get_D(*lst):
    #print([M*ones(shape(M)[1],1) for M in lst])
    return diag(*sum([ones(1, shape(M)[1])*M for M in lst], 
            zeros(1, shape(lst[0])[1])))


def get_diag_matricies(K, C, B):
    A = C - get_D(C, B)
    I = get_D(K)
    return A, I


def tuples_of_2Darray_from_2Darray_of_tuples(a):
    result = tuple([[] for i in range(len(a[0][0]))])
    for row in a:
        row_r = tuple([[] for i in range(len(a[0][0]))])
        for tup in row:
            for i, e in enumerate(tup):
                row_r[i].append(e)
        for i, r in enumerate(row_r):
            result[i].append(r)
    return result


def get_matricies_from_J_and_transition(J, transition_intensity_function):
    orbit_changes_matrix = [[transition_intensity_function(x, y)
        for x in J] for y in J]
    K, C, B = tuples_of_2Darray_from_2Darray_of_tuples(orbit_changes_matrix)
    return Matrix(K), Matrix(C), Matrix(B)


def simplify_to_an_array(*lst):
    result = [simplify(e).tolist() for e in lst]
    return tuple(result)

def get_ABKI(J, transition_function):
    K, C, B = get_matricies_from_J_and_transition(J, transition_function)
    A, I = get_diag_matricies(K, C, B)
    return simplify_to_an_array(A, B, K, I)


def m_phase_n_execution_transition_generator(M, N, lam, r0, r2, qs, us):
    def diff(z, y): 
        i_minus = M 
        i_plus = M 
        for i, (m, k) in enumerate(zip(z, y)):
            diff = m - k 
            if abs(diff) > 1: 
                return (M, M), False
            if diff == 1: 
                if i_plus == M: 
                    i_plus = i 
                else: 
                    return (M, M), False
            if diff == -1: 
                if i_minus == M: 
                    i_minus = i 
                else: 
                    return (M, M), False
        return (i_minus, i_plus), True

    r1 = 1 - r0 - r2
    def transition(y, z):
        (i_, i), result = diff(z, y)
        ps = (i != M)
        ms = (i_ != M)
        fulls = (sum(y) == N) 
        if (result == False):
            return (0, 0, 0)
        if (not ps and not ms):
            input_intensity = lam if fulls else 0
            no_change_intensity_sum = sum([y_*q*u*r1 for y_, q, u in zip(y, qs, us)])
            return (0, no_change_intensity_sum, input_intensity)
        if (ps and not ms and fulls):
            return (0, 0, 0)
        if (ps and not ms and not fulls):
            return (qs[i], qs[i]*lam, 0)
        if (ps and ms):
            return (0, y[i_]*qs[i]*us[i_]*r1, 0)
        if (not ps and ms):
            return (0, y[i_]*r0*us[i_], y[i_]*r2*us[i_])
        return (0, 0, 0)

    return transition


def m_phase_n_execution_sum_checker(N):
    def f(v):
        return (sum(v) <= N)
    return f


def m_phase_n_execution_check_all_states(m, n, f):
    return [v for v in itertools.product(range(m), repeat=n) if f(v)]


def m_phase_n_execution_J_gen(M, N):
    return m_phase_n_execution_check_all_states(N+1, M, 
        m_phase_n_execution_sum_checker(N))
     

def m_phase_n_execution_get_ABKI(M, N, lam, r0, r2, qs, us):
    J = m_phase_n_execution_J_gen(M, N)
    transition = m_phase_n_execution_transition_generator(M, N,
        lam, r0, r2, qs, us) 
    return get_ABKI(J, transition) 


