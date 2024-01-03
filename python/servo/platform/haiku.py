# Copyright 2023 The Servo Project Developers. See the COPYRIGHT
# file at the top-level directory of this distribution.
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

import os
import subprocess
import tempfile
from typing import Optional, Tuple

import distro
from .. import util
from .base import Base

HAIKU_PKGS = [
	'cmd:python3', 'cmd:gcc', 'cmd:git', 'cmd:curl', 'cmd:cmake',
	'cmd:rustc', 'cmd:pkg_config', 'cmd:m4', 'cmd:ccache',
	'llvm17', 'llvm17_clang',
	'setuptools_rust', 'gstreamer', 'gstreamer_devel', 'gst_plugins_good',
	'gst_plugins_bad',
]

#    'build-essential', 'ccache', 'clang', 'cmake', 'curl', 'g++', 'git',
#    'gperf', 'libdbus-1-dev', 'libfreetype6-dev', 'libgl1-mesa-dri',
#    'libgles2-mesa-dev', 'libglib2.0-dev', 'libgstreamer-plugins-bad1.0-dev',
#    'libgstreamer-plugins-base1.0-dev', 'libgstreamer1.0-dev',
#    'libharfbuzz-dev', 'liblzma-dev', 'libunwind-dev', 'libunwind-dev',
#    'libvulkan1', 'libx11-dev', 'libxcb-render0-dev', 'libxcb-shape0-dev',
#    'libxcb-xfixes0-dev', 'libxmu-dev', 'libxmu6', 'libegl1-mesa-dev',
#    'llvm-dev', 'm4', 'xorg-dev',

class Haiku(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_haiku = True
        (self.distro, self.version) = Haiku.get_distro_and_version()

    def library_path_variable_name(self):
        return "LIBRARY_PATH"

    @staticmethod
    def get_distro_and_version() -> Tuple[str, str]:
        distrib = distro.name()
        version = distro.version()
        return (distrib, version)

    def _platform_bootstrap(self, force: bool) -> bool:
        installed_something = self.install_dependencies(force)
        return installed_something

    def install_dependencies(self, force: bool) -> bool:
        install = False
        pkgs = HAIKU_PKGS
        command = ['pkgman', 'install', '-y'] + pkgs
        install = True
        if not install:
            return False

        def run_as_root(command, force=False):
            return subprocess.call(command)

        print("Installing missing dupendencies...")
        if subprocess.call(command) != 0:
            raise EnvironmentError("Installation of dependencies failed.")
        return True

    def gstreamer_root(self, cross_compilation_target: Optional[str]) -> Optional[str]:
        # GStreamer installed system-wide, we do not return a root in this
        # case because we don't have to update environment variables.
        return None
