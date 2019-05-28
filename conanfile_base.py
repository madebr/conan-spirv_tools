# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class ConanfileBase(ConanFile):
    _base_name = "spirv_tools"
    name = "spirv_cross"
    version = "2019.3"
    description = "SPIRV-Cross is a practical tool and library for performing reflection on SPIR-V and disassembling SPIR-V back to high level languages."
    topics = ("conan", "spirv", "assembly", "tool", )
    url = "https://github.com/bincrafters/conan-spirv_cross"
    homepage = "https://github.com/KhronosGroup/SPIRV-Cross"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "Apache-2.0"
    exports = ["LICENSE.md", ]
    exports_sources = ["CMakeLists.txt", ]
    no_copy_source = True
    generators = "cmake",

    _source_subfolder = "source_subfolder"

    def source(self):
        source_url = "https://github.com/KhronosGroup/SPIRV-Tools/archive/v{}.tar.gz".format(self.version)
        sha256 = "57c59584d83294ac914c1b21530f9441c29d30979a54e5f0a97b10715dc42c64"
        tools.get(source_url, sha256=sha256)
        os.rename("SPIRV-Tools-{}".format(self.version), self._source_subfolder)

        tools.replace_in_file(os.path.join(self._source_subfolder, "source", "CMakeLists.txt"),
                                           " SHARED ",
                                           " ")

    @property
    def _spirv_headers_req(self):
        return "spirv-headers/1.4.1@{}/{}".format(self.user, self.channel)

    def requirements(self):
        if not self._installer:
            self.requires(self._spirv_headers_req)

    def build_requirements(self):
        if self._installer:
            self.build_requires(self._spirv_headers_req)

    @property
    def _build_type(self):
        return self.settings.build_type if self.settings.get_safe("build_type") else "Release"

    def build(self):
        cmake = CMake(self)

        cmake_defines = {
            "SPIRV_BUILD_COMPRESSION": True,
            "SPIRV_LOG_DEBUG": self._build_type == "Debug",
            "SPIRV_CHECK_CONTEXT": self._build_type == "Debug",
            "SPIRV_SKIP_TESTS": True,
            "SPIRV-Headers_SOURCE_DIR": self.deps_cpp_info["spirv-headers"].rootpath,
            "SPIRV_SKIP_EXECUTABLES": not self._installer,
        }
        cmake.configure(defs=cmake_defines)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install(build_dir=self.build_folder)

        self.copy("LICENSE", src=self._source_subfolder, dst="licenses")

        try:
            shutil.rmtree(os.path.join(self.package_folder, "lib", "pkgconfig"))
        except FileNotFoundError:
            pass
