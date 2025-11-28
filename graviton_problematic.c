/*
 * graviton_problematic.c - Example C file with many Graviton migration issues
 * This file intentionally contains architecture-specific code, deprecated APIs,
 * and x86-specific intrinsics to demonstrate high-effort migration challenges
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <emmintrin.h>      // SSE2 intrinsics (x86-specific)
#include <immintrin.h>      // AVX2 intrinsics (x86-specific)
#include <cpuid.h>          // x86 CPUID instruction
#include <x86intrin.h>      // More x86 intrinsics

// Deprecated POSIX functions that may have ARM64 compatibility issues
#include <sys/time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

// Old OpenSSL 1.0.x (known ARM64 compatibility issues)
#include <openssl/ssl.h>
#include <openssl/err.h>

// Old libcurl with deprecated APIs
#include <curl/curl.h>

// Old zlib with potential ARM64 issues
#include <zlib.h>

// Old ncurses library (ARM64 porting challenges)
#include <ncurses.h>

// Architecture-specific assembly
void x86_cpuid_test() {
    unsigned int eax, ebx, ecx, edx;
    __cpuid(1, eax, ebx, ecx, edx);  // x86 CPUID instruction - WON'T WORK ON ARM64
    if (ecx & (1 << 9)) {
        printf("SSE2 supported\n");
    }
}

// SSE2 intrinsics - x86 only
void sse2_matrix_multiply(float* A, float* B, float* C, int n) {
    int i;
    for (i = 0; i < n; i += 4) {
        __m128 a = _mm_load_ps(&A[i]);
        __m128 b = _mm_load_ps(&B[i]);
        __m128 result = _mm_mul_ps(a, b);
        _mm_store_ps(&C[i], result);
    }
}

// AVX2 intrinsics - x86 only
void avx2_vector_add(float* a, float* b, float* result, int n) {
    int i;
    for (i = 0; i < n; i += 8) {
        __m256 va = _mm256_load_ps(&a[i]);
        __m256 vb = _mm256_load_ps(&b[i]);
        __m256 vr = _mm256_add_ps(va, vb);
        _mm256_store_ps(&result, vr);
    }
}

// RDTSC instruction - x86 performance counter (ARM64 needs PMCCNTR_EL0)
unsigned long long get_cycles_x86() {
    unsigned int lo, hi;
    __asm__ volatile ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((unsigned long long)hi << 32) | lo;
}

// Old OpenSSL 1.0.x API (deprecated and ARM64 issues)
void old_openssl_init() {
    SSL_library_init();
    SSL_load_error_strings();
    OpenSSL_add_all_algorithms();
}

// Old libcurl API with deprecated options
size_t write_callback(void* contents, size_t size, size_t nmemb, void* userp) {
    return size * nmemb;
}

void old_curl_request() {
    CURL* curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "https://example.com");
        curl_easy_setopt(curl, CURLOPT_SSLVERSION, CURL_SSLVERSION_TLSv1);  // Deprecated
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
}

// Old zlib API usage
void compress_old_zlib(unsigned char* input, unsigned long input_len, 
                      unsigned char* output, unsigned long* output_len) {
    compress(output, output_len, input, input_len);  // Old API
}

// Old ncurses API
void old_ncurses_interface() {
    initscr();
    start_color();
    init_pair(1, COLOR_GREEN, COLOR_BLACK);
    attron(COLOR_PAIR(1));
    printw("Old ncurses interface");
    refresh();
    getch();
    endwin();
}

// x86-specific bit manipulation using BMI2 instructions
uint64_t x86_bmi2_popcnt(uint64_t x) {
    return _pdep_u64(x, 0xAAAAAAAAAAAAAAAAULL);  // BMI2 instruction
}

// Old socket programming with deprecated getsockname API
int create_old_socket() {
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd >= 0) {
        struct sockaddr_in addr;
        socklen_t len = sizeof(addr);
        getsockname(sockfd, (struct sockaddr*)&addr, &len);  // Deprecated on some systems
    }
    return sockfd;
}

// Multiple x86 FPU instructions
void x86_fpu_test() {
    double a = 1.0, b = 2.0;
    __asm__ volatile (
        "fld %1\n"
        "fld %2\n"
        "faddp\n"
        "fstp %0"
        : "=m"(a)
        : "m"(a), "m"(b)
    );
}

// Old gettimeofday usage (higher precision alternatives needed on ARM64)
void old_timing() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
}

// Even more SSE intrinsics
void sse_crypto_hash(unsigned char* data, int len) {
    __m128i state = _mm_setzero_si128();
    for (int i = 0; i < len; i += 16) {
        __m128i block = _mm_loadu_si128((__m128i*)&data[i]);
        state = _mm_xor_si128(state, block);
    }
}

int main() {
    printf("Graviton Migration Test - High Complexity\n");
    
    x86_cpuid_test();
    sse2_matrix_multiply(NULL, NULL, NULL, 16);
    avx2_vector_add(NULL, NULL, NULL, 32);
    printf("Cycles: %llu\n", get_cycles_x86());
    old_openssl_init();
    old_curl_request();
    compress_old_zlib(NULL, 0, NULL, NULL);
    old_ncurses_interface();
    create_old_socket();
    x86_fpu_test();
    old_timing();
    
    printf("This file has 47+ migration issues!\n");
    return 0;
}