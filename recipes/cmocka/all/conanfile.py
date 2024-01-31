from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rmdir, save
from conan.tools.scm import Version
import os
import textwrap

required_conan_version = ">=1.53.0"


class CmockaConan(ConanFile):
    name = "cmocka"
    license = "Apache-2.0"
    homepage = "https://cmocka.org"
    url = "https://github.com/conan-io/conan-center-index"
    description = "A unit testing framework for C"
    topics = ("unit_test", "unittest", "test", "testing", "mock", "mocking")

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    
    exports_sources="./*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        self.settings.rm_safe("compiler.cppstd")
        self.settings.rm_safe("compiler.libcxx")

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.variables["WITH_EXAMPLES"] = False
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if (not self.conf.get("tools.build:skip_test", default=False)) and can_run(self):
            cmake.test()

    def package(self):
        copy(self, "COPYING", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        self._create_cmake_module_variables(
            os.path.join(self.package_folder, self._module_file_rel_path)
        )

    def _create_cmake_module_variables(self, module_file):
        content = textwrap.dedent("""\
            if(NOT DEFINED CMOCKA_INCLUDE_DIR)
                set(CMOCKA_INCLUDE_DIR ${cmocka_INCLUDE_DIRS}
                                       ${cmocka_INCLUDE_DIRS_RELEASE}
                                       ${cmocka_INCLUDE_DIRS_RELWITHDEBINFO}
                                       ${cmocka_INCLUDE_DIRS_MINSIZEREL}
                                       ${cmocka_INCLUDE_DIRS_DEBUG})
            endif()
            if(TARGET cmocka::cmocka)
                if(NOT DEFINED CMOCKA_LIBRARY)
                    set(CMOCKA_LIBRARY cmocka::cmocka)
                endif()
                if(NOT DEFINED CMOCKA_LIBRARIES)
                    set(CMOCKA_LIBRARIES cmocka::cmocka)
                endif()
            endif()
        """)
        save(self, module_file, content)

    @property
    def _module_file_rel_path(self):
        return os.path.join("lib", "cmake", f"conan-official-{self.name}-variables.cmake")

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "cmocka")
        self.cpp_info.set_property("pkg_config_name", "cmocka")
        self.cpp_info.set_property("cmake_build_modules", [self._module_file_rel_path])
        lib_suffix = ""
        if Version(self.version) < "1.1.7" and not self.options.shared:
            lib_suffix = "-static"
        self.cpp_info.libs = ["cmocka" + lib_suffix]

        cmake_files_path=os.path.join(self.package_folder, "lib", "cmake", "cmocka")
        cmake_files=os.listdir(cmake_files_path)
        paths=[os.path.join(cmake_files_path, file) for file in cmake_files]+[self._module_file_rel_path]
        self.cpp_info.set_property(
            "cmake_build_modules", paths
        )