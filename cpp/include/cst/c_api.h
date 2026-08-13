#ifndef CST_C_API_H
#define CST_C_API_H
#include <stddef.h>
#if defined(_WIN32)
#if defined(CST_CAPI_BUILD)
#define CST_API __declspec(dllexport)
#else
#define CST_API __declspec(dllimport)
#endif
#else
#define CST_API __attribute__((visibility("default")))
#endif
#ifdef __cplusplus
extern "C" {
#endif
#define CST_OK 0
#define CST_ERR_NULL 1
#define CST_ERR_ARGUMENT 2
CST_API int cst_synaptic_affinity(const double* a,const double* b,size_t len,double sigma,double* out_value);
CST_API int cst_synaptic_matrix(const double* states,size_t rows,size_t cols,double sigma,double* out_matrix);
CST_API int cst_synaptic_blend(double standard,double affinity,double gate,double* out_value);
CST_API int cst_synaptic_state_step(double* state,const double* signal,size_t len,double decay,double gain,double dt);
CST_API const char* cst_synaptic_spec_version(void);
#ifdef __cplusplus
}
#endif
#endif
