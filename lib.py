from sympy import Matrix
import numpy as np


def value_eval(q, y, z, arg_dict, temp_arg_dict, value_function_lst):
    return [f(q, y, z, arg_dict, temp_arg_dict) for f in value_function_lst]


def eval_value_function_list_if_check(
        q, y, z, const_arg, arg, check_f, value_f_lst):
    if check_f(q, y, z, const_arg, arg):
        return value_eval(q, y, z, const_arg, arg, value_f_lst)
    else:
        return []


def eval_function_list(q, y, z, const_arg, arg, function_lst):
    if (len(function_lst) > 1):
        check_f = function_lst[0]
        value_f_lst = function_lst[1:]
        return eval_value_function_list_if_check(q, y, z,
            const_arg, arg, check_f, value_f_lst)
    else:
        return []


def eval_LFL_with_local_arg(q, y, z, const_arg, LFL, local_arg):
    for f in LFL:
        e = eval_function_list(q, y, z, const_arg, local_arg, f)
        if e:
            return e
    return []


def eval_LFL(q, y, z, const_arg, LFL, create_arg):
    if (q == 0) and (y == z):
        return []
    else:
        local_arg = create_arg(q, y, z, const_arg)
        return eval_LFL_with_local_arg(q, y, z, 
            const_arg, LFL, local_arg)


def fill_to_standart_size(lst, n):
    return lst + [0]*(n-len(lst))


def create_state_matrix_with_polynom_inside(
        q, J, N, const_arg, list_of_function_list, create_arg):
    return [[fill_to_standart_size(
        eval_LFL(q, y, z, const_arg, list_of_function_list, create_arg),
                N) for z in J] for y in J]


def transpose_state_matrix_inside(Mq):
    return [Matrix(m) for m in np.transpose(Mq, axes=(2, 0, 1)).tolist()]


def create_orbit_change_row(
        q, J, N, const_arg, list_of_function_list, create_arg):
    return transpose_state_matrix_inside(
        create_state_matrix_with_polynom_inside(
            q, J, N, const_arg, list_of_function_list, create_arg))


def algorithm(J, N, W, const_arg, list_of_function_list,
        create_arg=lambda q, z, y, arg_dict: {}):
    return [create_orbit_change_row(
            q, J, N+1, const_arg, list_of_function_list, create_arg)
        for q in range(-1, W + 1)]
