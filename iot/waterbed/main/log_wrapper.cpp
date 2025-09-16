#include "esp_log.h"
#include <stdarg.h>

// Forward declarations for the real (unwrapped) functions
extern "C" void __real_esp_log_writev(esp_log_level_t level, const char* tag, const char* format, va_list args);
extern "C" void __real_esp_log_write(esp_log_level_t level, const char* tag, const char* format, ...);

// Wrapper implementation for ESP diagnostics log wrapping
// This is called by the esp_diagnostics component when it wraps esp_log_writev
extern "C" void __wrap_esp_log_writev(esp_log_level_t level, const char* tag, const char* format, va_list args) {
    // Call the real function to avoid infinite recursion
    __real_esp_log_writev(level, tag, format, args);
}

// Wrapper implementation for ESP diagnostics log wrapping  
// This is called by the esp_diagnostics component when it wraps esp_log_write
extern "C" void __wrap_esp_log_write(esp_log_level_t level, const char* tag, const char* format, ...) {
    va_list args;
    va_start(args, format);
    __real_esp_log_writev(level, tag, format, args);
    va_end(args);
}
