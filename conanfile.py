# -*- coding: utf-8 -*-

from conanfile_base import ConanfileBase
from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os
import re
import shutil


class Conanfile(ConanfileBase):
    name = "spirv_tools"
    version = ConanfileBase.version
    exports = ConanfileBase.exports + ["conanfile_base.py"]

    settings = "os", "arch", "compiler", "build_type",
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    _installer = False

    def configure(self):
        if self.options.shared or self.settings.os == "Windows":
            del self.options.fPIC

    def package(self):
        super(Conanfile, self).package()
        bindir = os.path.join(self.package_folder, "bin")
        if os.path.isdir(bindir):
            shutil.rmtree(bindir)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
