#include "esp_log.h"
#include <stdarg.h>

int __wrap_esp_log_writev(esp_log_level_t level,
                          const char *tag,
                          const char *format,
                          va_list args) {
    return esp_log_writev(level, tag, format, args);
}

int __wrap_esp_log_write(esp_log_level_t level,
                         const char *tag,
                         const char *format, ...) {
    va_list ap;
    va_start(ap, format);
    int r = esp_log_writev(level, tag, format, ap);
    va_end(ap);
    return r;
}
