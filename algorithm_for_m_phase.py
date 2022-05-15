import sys
from m_phase_n_execution import get_ABKI
from _four_matricies_to_diffusion_asymptotic import ffi, lib
import numpy as np

def python_square_matrix_to_cffi_array(m):
    line_from_square = []
    for s in m:
        line_from_square += list(s)
    result = ffi.new("double[]", len(line_from_square)) 
    for i, l in enumerate(line_from_square):
        result[i] = l
    print(list(result))
    return result

def get_rabp(m, n, sigma, lam, qs, mus, r0, r2, x_n, percision):
    A, B, K, I = get_ABKI(m, n, lam, qs, mus, r0, r2)
    matrix_dim = len(A)
    A_ptr = python_square_matrix_to_cffi_array(A)
    B_ptr = python_square_matrix_to_cffi_array(B)
    K_ptr = python_square_matrix_to_cffi_array(K)
    I_ptr = python_square_matrix_to_cffi_array(I)
    a_b = ffi.new("double[]", x_n)
    a = ffi.new("double[]", x_n)
    b = ffi.new("double[]", x_n)
    r = ffi.new("double[]", x_n*matrix_dim)
    lib.charge_a_b_integral(
        a_b, a, b, r,
        A_ptr, B_ptr, K_ptr, I_ptr,
        matrix_dim, x_n, percision)
    np_a_b =  np.array(ffi.buffer(a_b))
    np_a = np.array(ffi.buffer(a))
    np_b = np.array(ffi.buffer(b))
    np_r = np.array(ffi.buffer(r))
    np_pi = np.exp(2*np_a_b/sigma)/np_b
    print(np_pi)
    np_orbit_distribution = np_pi/sum(np_pi)
    r_out = np_r.astype(np.float64)
    a_out = np_a.astype(np.float64)
    b_out = np_b.astype(np.float64)
    p_out = np_orbit_distribution.astype(np.float64)
    return r_out, a_out, b_out, p_out

def write_double_array_to_file(a, filename):
    with open(filename, "w") as f:
        for d in a:
            f.write(str(d) + "\n")

def main():
    r_filename = sys.argv[1] 
    a_filename = sys.argv[2] 
    b_filename = sys.argv[3] 
    p_filename = sys.argv[4]
    for sf in sys.argv[5:]:
        if (float(sf) < 0):
            printf("negative argument")
            return 1
    n = int(sys.argv[5])
    sigma_value = float(sys.argv[6])
    lambda_value = float(sys.argv[7])
    r0_value = float(sys.argv[8])
    r2_value = float(sys.argv[9])
    x_n = int(sys.argv[10])
    percision = float(sys.argv[11])
    number_of_fixed_args = 12
    if ((r0_value + r2_value) > 1):
        printf("r0 + r2 bigger then one")
        return 1
    number_of_rest_args = len(sys.argv) - number_of_fixed_args
    if ((number_of_rest_args % 2) == 0):
        printf("wrong number of arguuments")
        return 1
    number_of_phases = (number_of_rest_args + 1) // 2
    number_of_qus = number_of_phases - 1
    string_qs = sys.argv[number_of_fixed_args: 
        number_of_fixed_args + number_of_qus]
    qs = [float(q) for q in string_qs]
    if (sum(qs) > 1):
        printf("sum of qs bigger then one")
        return 1
    string_mus = sys.argv[number_of_fixed_args + number_of_qus:]
    mus = [float(mu) for mu in string_mus]
    r, a, b, p = get_rabp(number_of_phases, n, 
        sigma_value, lambda_value, qs, mus, r0_value, r2_value, x_n, percision)
    write_double_array_to_file(r, r_filename)
    write_double_array_to_file(a, a_filename)
    write_double_array_to_file(b, b_filename)
    write_double_array_to_file(p, p_filename)
    return 0


if __name__ == "__main__":
    main()
