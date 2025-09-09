# ESP32
microcontroller

## PlatformIO
- PlatformIO: instead of Arduino IDE to connect and upload binaries to microcontroller

## ESP-IDF
### Install Mac
[Install instructions source](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/get-started/linux-macos-setup.html)\
`brew install cmake ninja dfu-util`\
`brew install ccache` for faster builds\
Then clone esp-idf repo, and setup\
`mkdir -p ~/dev/esp`\
`cd ~/dev/esp`\
`git clone -b v5.5.1 --recursive https://github.com/espressif/esp-idf.git`\
`cd ~/dev/esp/esp-idf`\
`./install.sh <esp32c3|devices>` e.g. "esp32c3, esp32c6" or "all".\
Set path to scripts\
`export IDF_TOOLS_PATH="$HOME/required_idf_tools_path"`\
`./install.sh`\
`. ./export.sh`\
Run this in terminal to load curr path as executables\
`. $HOME/dev/esp/esp-idf/export.sh`
Must do this at every terminal, or run get_idf with:\
`alias get_idf='. $HOME/dev/esp/esp-idf/export.sh'`\
### Usage
Navigate to project and run:\
`idf.py set-target esp32c3` # running this clears build cache. Target saved in env variables can bypass this step.\
`idf.py menuconfig`\
Navigate to project directory\
`cd ~/esp/hello_world`\
`rm -rf build` # may need to delete build dir before set-target\
`idf.py set-target esp32c3`\
`idf.py menuconfig`\
Build project # can skip this if running flash (flash does both)\
`idf.py build`\
Plug in esp32 and check port\
`ls /dev/cu.*` mine is `/dev/cu.usbmodem2101`\
Flash to esp with port\
`idf.py -p /dev/cu.usbmodem2101 flash` # if port not provided, idf will try to guess \
Monitor:\
`idf.py -p /dev/cu.usbmodem2101 monitor`\
Exit monitor with `control + ]`

### On restart of terminal
`idf.py set-target esp32c3`\
`idf.py build flash monitor -p /dev/cu.usbmodem2101`



### Install arduino to make life easier
idf.py add-dependency "espressif/arduino-esp32^3.3.0"\
Link code to arduino, in CMakeLists.txt:
```
idf_component_register(SRCS "main.cpp" INCLUDE_DIRS ".")
target_link_libraries(${COMPONENT_LIB} PUBLIC arduino-esp32)
```
