cmake -D CMAKE_TOOLCHAIN_FILE=/home/clandinin/lib/vcpkg/scripts/buildsystems/vcpkg.cmake -D PGR_USB3=ON -D PGR_DIR=/opt/spinnaker/ ..
cmake --build . --config Release -- -j 4
