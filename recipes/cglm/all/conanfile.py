# from conans import ConanFile, CMake, tools
import os
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import get
from conan.tools.build import can_run

required_conan_version = ">=2.0"


class CglmConan(ConanFile):
    name = "cglm"
    description = "Highly Optimized Graphics Math (glm) for C "
    topics = ("cglm", "graphics", "opengl", "simd", "vector", "glm")
    homepage = "https://github.com/recp/cglm"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = "CMakeLists.txt", "src/*", "include/*", "test/*"
    generators = "cmake"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "header_only": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "header_only": False,
    }
    generators = "CMakeDeps"

    def requirements(self):
        self.tool_requires("cmake/[~3]")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        if self.options.header_only:
            del self.settings.arch
            del self.settings.build_type
            del self.settings.compiler
            del self.settings.os

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    # def build(self):
    #     for patch in self.conan_data.get("patches", {}).get(self.version, []):
    #         tools.patch(**patch)

    #     if not self.options.header_only:
    #         cmake = self._configure_cmake()
    #         cmake.build()
    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["CGLM_STATIC"] = not self.options.shared
        tc.cache_variables["CGLM_SHARED"] = self.options.shared
        # if not self.conf.get("tools.build:skip_test", default=False):
        tc.cache_variables["CGLM_USE_TEST"] = (
            not self.conf.get("tools.build:skip_test", default=False))
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if not self.conf.get("tools.build:skip_test", default=False):
            cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    # def package(self):
    #     self.copy("LICENSE", src=self._source_subfolder, dst="licenses")

    #     if self.options.header_only:
    #         self.copy("*", src=os.path.join(self._source_subfolder, "include"), dst="include")
    #     else:
    #         cmake = self._configure_cmake()
    #         cmake.install()

    #         tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
    #         tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    # def package_info(self):
    #     self.cpp_info.set_property("cmake_file_name", "cglm")
    #     self.cpp_info.set_property("cmake_target_name", "cglm::cglm")
    #     self.cpp_info.set_property("pkg_config_name", "cglm")

    #     if not self.options.header_only:
    #         self.cpp_info.libs = ["cglm"]
    #         if self.settings.os in ("Linux", "FreeBSD"):
    #             self.cpp_info.system_libs.append("m")

    #     # backward support of cmake_find_package, cmake_find_package_multi & pkg_config generators
    #     self.cpp_info.names["pkg_config"] = "cglm"
    #     self.cpp_info.names["cmake_find_package"] = "cglm"
    #     self.cpp_info.names["cmake_find_package_multi"] = "cglm"
