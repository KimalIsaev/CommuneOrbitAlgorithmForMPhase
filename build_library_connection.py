from cffi import FFI

FFI_BUILDER = FFI()

C_FILE_NAME = "_four_matricies_to_diffusion_asymptotic"

HEADER = '''
void
charge_a_b_integral(
    double* a_b_integral, double* a, double* b, double* r,
    double* A, double* B, double* K, double* I,
    unsigned int n, unsigned int x_n, double x_delta);
'''
C_FILE = '''
#include "four_matricies_to_diffusion_asymptotic.h"
'''
FFI_BUILDER.cdef(HEADER)
FFI_BUILDER.set_source(C_FILE_NAME, C_FILE, 
    libraries=["four_matricies_to_diffusion_asymptotic"],
    library_dirs=["FourMatriciesToDiffusionAsymptotic"],
    include_dirs=["FourMatriciesToDiffusionAsymptotic"]
)

if __name__ == "__main__":
    FFI_BUILDER.compile(verbose=True)

