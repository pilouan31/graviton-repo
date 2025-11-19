#include <stdio.h>
#include <stdint.h>
#include <cpuid.h>
#include <immintrin.h>

// x86-specific CPUID function using inline assembly
void get_cpu_vendor(char* vendor) {
    uint32_t eax, ebx, ecx, edx;
    __asm__ volatile("cpuid"
                     : "=a" (eax), "=b" (ebx), "=c" (ecx), "=d" (edx)
                     : "a" (0));
    
    *((uint32_t*)vendor) = ebx;
    *((uint32_t*)(vendor + 4)) = edx;
    *((uint32_t*)(vendor + 8)) = ecx;
    vendor[12] = '\0';
}

// x86 timestamp counter using inline assembly
uint64_t rdtsc() {
    uint32_t low, high;
    __asm__ volatile("rdtsc" : "=a" (low), "=d" (high));
    return ((uint64_t)high << 32) | low;
}

// SSE intrinsics - x86 specific
void sse_operations() {
    __m128 a = _mm_set_ps(1.0f, 2.0f, 3.0f, 4.0f);
    __m128 b = _mm_set_ps(5.0f, 6.0f, 7.0f, 8.0f);
    __m128 result = _mm_add_ps(a, b);
    
    // More SSE operations
    __m128 mul_result = _mm_mul_ps(a, b);
    __m128 div_result = _mm_div_ps(a, b);
}

// AVX intrinsics - x86 specific
void avx_operations() {
    __m256 a = _mm256_set_ps(1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f, 8.0f);
    __m256 b = _mm256_set_ps(8.0f, 7.0f, 6.0f, 5.0f, 4.0f, 3.0f, 2.0f, 1.0f);
    __m256 result = _mm256_add_ps(a, b);
    
    // AVX2 operations
    __m256i int_a = _mm256_set1_epi32(42);
    __m256i int_b = _mm256_set1_epi32(24);
    __m256i int_result = _mm256_add_epi32(int_a, int_b);
}

// AVX-512 intrinsics - latest x86 specific
void avx512_operations() {
    __m512 a = _mm512_set1_ps(1.0f);
    __m512 b = _mm512_set1_ps(2.0f);
    __m512 result = _mm512_add_ps(a, b);
}

// x86 pause instruction using inline assembly
void cpu_pause() {
    __asm__ volatile("pause" ::: "memory");
}

// Memory fence using x86 assembly
void memory_fence() {
    __asm__ volatile("mfence" ::: "memory");
}

// x86 specific MSR operations
void read_msr(uint32_t msr, uint32_t* low, uint32_t* high) {
    __asm__ volatile("rdmsr" : "=a" (*low), "=d" (*high) : "c" (msr));
}

// x86 specific performance counter
uint64_t read_pmc(uint32_t counter) {
    uint32_t low, high;
    __asm__ volatile("rdpmc" : "=a" (low), "=d" (high) : "c" (counter));
    return ((uint64_t)high << 32) | low;
}

int main() {
    char vendor[13];
    get_cpu_vendor(vendor);
    printf("CPU Vendor: %s\n", vendor);
    
    uint64_t cycles = rdtsc();
    printf("Timestamp: %lu\n", cycles);
    
    sse_operations();
    avx_operations();
    avx512_operations();
    
    cpu_pause();
    memory_fence();
    
    return 0;
}