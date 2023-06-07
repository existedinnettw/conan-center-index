from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
import os
from conan.tools.build import can_run


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    # generators = "cmake"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self)

    def test(self):
        # if not tools.cross_building(self.settings):
        if can_run(self):
            # bin_path = os.path.join("bin", "test_package")
            # self.run(bin_path, run_environment=True)
            cmd = os.path.join(self.cpp.build.bindir, "test_package")
            self.run(cmd, env="conanrun")
