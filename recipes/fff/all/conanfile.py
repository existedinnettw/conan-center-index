from conan import ConanFile
import os
from conan.tools.files import get, copy
from conan.tools.cmake import cmake_layout, CMake
from conan.tools.scm import Version
from conan.tools.scm.git import Git

class TypeSafe(ConanFile):
    name = 'fff'
    settings = "os", "arch", "compiler", "build_type"
    
    description = 'A testing micro framework for creating function test doubles'
    url = 'https://github.com/conan-io/conan-center-index'
    homepage = 'https://github.com/meekrosoft/fff'
    license = 'MIT'
    topics = 'conan', 'c', 'c++', 'embedded', 'tdd', 'micro-framework', 'fake-functions'

    exports_sources = "*.h", "CMakeLists.txt", "test/*"
    no_copy_source = True
    generators = "CMakeToolchain", "CMakeDeps"

    # @property
    # def _source_subfolder(self):
    #     return "source_subfolder"

    def requirements(self):
        self.build_requires("cmake/[>=3.15 <3.26]")
        self.test_requires("gtest/[~1.12]")

    def layout(self):
        cmake_layout(self)

    def build(self):
        '''
        depend on v1.1 or not. Newest commit add cmake support, which is great
        '''
        if Version(self.version) > "1.1":
            if not self.conf.get("tools.build:skip_test", default=False):
                cmake = CMake(self)
                cmake.configure(cli_args=["-DFFF_UNIT_TESTING=True"])
                cmake.build()
                cmake.test()

    def source(self):
        get(self, **self.conan_data["sources"][self.version]) #, destination=self._source_subfolder

    def package(self):
        path=os.path.join(self.package_folder, 'include')
        copy(self, "*.h", self.source_folder, path)

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []

    def package_id(self):
        # self.info.header_only()
        self.info.clear()
