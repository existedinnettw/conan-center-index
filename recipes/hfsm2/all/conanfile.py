import os.path

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, rmdir


class HFSM2(ConanFile):
    name = "hfsm2"
    description = " High-Performance Hierarchical Finite State Machine Framework "
    license = "MIT"
    url = "https://github.com/andrew-gresyk/HFSM2"
    homepage = "https://github.com/andrew-gresyk/HFSM2"
    topics = "fsm", "header-only", "cpp11"

    # header only
    # https://docs.conan.io/2/tutorial/creating_packages/other_types_of_packages/header_only_packages.html?highlight=no_copy_source
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = "include/*", "test/*"
    no_copy_source = True

    def requirements(self):
        self.test_requires("doctest/2.4.11")
        # self.test_requires("xoshiro-cpp/1.1") #require cpp17, and for development only
        self.tool_requires("cmake/[>=3.15 <4]")

    def validate(self):
        check_min_cppstd(self, 11)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        cmake = CMakeDeps(self)
        cmake.generate()

    def build(self):
        # cmake = CMake(self)
        # cmake.configure()
        # cmake.build()
        # hfsm2 not yet implement it in cmake.
        # if not self.conf.get("tools.build:skip_test", default=False):
        #     cmake = CMake(self)
        #     cmake.configure(build_script_folder="test")
        #     cmake.build()
        #     self.run(os.path.join(self.cpp.build.bindir, "test_sum"))
        #     cmake.test()
        pass

    def package(self):
        # This will also copy the "include" folder
        copy(self, "*.hpp", self.source_folder, self.package_folder)

    def package_info(self):
        # For header-only packages, libdirs and bindirs are not used
        # so it's necessary to set those as empty.
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []

    def package_id(self):
        self.info.clear()
