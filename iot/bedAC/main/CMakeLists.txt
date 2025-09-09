idf_component_register(
    SRCS "main.cpp" "log_wrap_shim.c"
    PRIV_REQUIRES spi_flash
    INCLUDE_DIRS "."
    REQUIRES arduino-esp32
)
