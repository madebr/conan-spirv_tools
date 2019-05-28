# -*- coding: utf-8 -*-

from conans import CMake, ConanFile, tools
import os


class TestPackageConan(ConanFile):

    def test(self):
        bins = [
            "spirv-as",
            "spirv-as",
            "spirv-cfg",
            "spirv-dis",
            # "spirv-lesspipe.sh",
            "spirv-link",
            "spirv-markv",
            "spirv-opt",
            "spirv-reduce",
            "spirv-stats",
            "spirv-val",
        ]
        for bin in bins:
            if not tools.cross_building(self.settings):
                self.run("{} --help".format(bin))
