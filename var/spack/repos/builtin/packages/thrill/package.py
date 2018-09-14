##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

import os


class Thrill(CMakePackage):
    """An EXPERIMENTAL Algorithmic Distributed Big Data Batch Processing
    Framework in C++.
    """

    homepage = "http://www.project-thrill.org"

    version('master',
            git='https://github.com/ivotron/thrill.git',
            branch='foxxllfix',
            submodules=True)

    variant('mpi', default=True, description="Enable MPI net backend.")

    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        args = ['-DTHRILL_BUILD_EXAMPLES=ON']
        return args

    def install(self, spec, prefix):
        """Since Thrill CMake configuration does not install examples, we need
        to override the CMakePackage.install() method so that we look for
        binaries and move them to the binary install folder.
        """

        # call parent
        super(Thrill, self).install(spec, prefix)

        examples_dir = self.build_directory + '/examples'
        for ex in os.listdir(examples_dir):
            expath = os.path.join(examples_dir, ex)
            if not os.path.isdir(expath):
                continue
            for f in os.listdir(expath):
                fpath = os.path.join(expath, f)
                if os.path.isfile(fpath) and os.access(fpath, os.X_OK):
                        install(fpath, prefix.bin)
