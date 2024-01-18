import os
import re
from conan import ConanFile
from conan.tools.cmake import CMakeDeps, CMake, CMakeToolchain, cmake_layout
from conan.tools import files
from conan.tools.files import copy
from pathlib import Path


def get_version():
    try:
        version = "1.4.5"
        return version.strip()
    except Exception:
        return None


class TufaoConan(ConanFile):
    name = "tufao"
    version = get_version()
    #author = "Mateusz Pusz"
    #license = "https://github.com/mpusz/new-project-template/blob/master/LICENSE"
    url = "https://github.com/LogosDesignAS/tufao"
    description = "An asynchronous web framework for C++ built on top of Qt "
    #exports = ["LICENSE.md"]
    settings = "os", "compiler", "build_type", "arch"

    options = {   # remove for a header-only library
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": True,    # remove for a header-only library
        "fPIC": True,       # remove for a header-only library
    }

    generators = "CMakeDeps"

    exports_sources = ('CMakeLists.txt', 'src/*', 'tests/*', 'TufaoConfig.cmake.in', 'COPYING.LESSER', 'cmake/*',
                       'include/*', 'doc/*', '3rd/*')

    def requirements(self):
        self.requires('boost/1.83.0')

    def configure(self):
        self.options["Tufao"].shared = True

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC   # remove for a header-only library

    def layout(self):
        cmake_layout(self)
        self.folders.build = "conan/build"
        self.folders.generators = "conan"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.presets_prefix = Path(self.folders._base_build).name
        tc.generate()


    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()


    def package(self):
        cmake = CMake(self)
        cmake.install()

    @property
    def _postfix(self):
        if self.settings.os == "Windows":
            return "d" if self.settings.build_type == "Debug" else ""

    def package_info(self):
        self.cpp_info.libs = ["Tufao"]
        self.cpp_info.set_property("cmake_find_mode", "none") # do not generate find modules
        self.cpp_info.builddirs.append(os.path.join("lib", "cmake", "Tufao"))
        self.cpp_info.set_property("cmake_file_name", "Tufao")
        self.cpp_info.set_property("cmake_target_name", "Tufao::Tufao")

    # uncomment for a header-only library
    # def package_id(self):
    #     self.info.header_only()
