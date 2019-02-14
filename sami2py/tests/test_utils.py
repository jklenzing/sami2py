#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
# -----------------------------------------------------------------------------
""" Tests the utilities functions
"""

from __future__ import (print_function)
import os
import sami2py
from nose.tools import raises


class TestGeneratePath():
    """Test basic functionality of the generate_path function
    """
    def setup(self):
        """Runs before every method to create a clean testing setup."""
        sami2py.archive_dir = 'test'

    def test_successful_path_generation(self):
        """Tests generation of a path that is successful"""
        out_path = sami2py.utils.generate_path(tag='test', lon=0, year=2012,
                                               day=277, test=True)
        assert out_path == sami2py.test_data_dir + '/test/lon000/2012_277/'

    @raises(NameError)
    def test_generate_path_w_blank_archive_dir(self):
        """Tests generation of a path without archive_dir set"""
        sami2py.archive_dir = ''
        sami2py.utils.generate_path(tag='test', lon=0, year=2012, day=277)

    @raises(TypeError)
    def test_generate_path_w_numeric_tag(self):
        """Tests generation of a path with a numeric tag"""

        sami2py.utils.generate_path(tag=7, lon=0, year=2012, day=277)

    @raises(ValueError)
    def test_generate_path_w_nonnumeric_lon(self):
        """Tests generation of a path with a nonnumeric longitude"""

        sami2py.utils.generate_path(tag='test', lon='0', year=2012, day=277)

    @raises(ValueError)
    def test_generate_path_w_nonnumeric_year(self):
        """Tests generation of a path with a nonnumeric year"""

        sami2py.utils.generate_path(tag='test', lon=0, year='2012', day=277)

    @raises(ValueError)
    def test_generate_path_w_nonnumeric_day(self):
        """Tests generation of a path with a nonnumeric day"""

        sami2py.utils.generate_path(tag='test', lon=0, year=2012, day='277')


class TestArchiveDir():
    """Test basic functionality of the set_archive_dir function
    """
    def test_set_archive_dir(self):
        """Test that set_archive_dir has set and stored the archive directory

           To leave the archive directory unchanged it must be gathered and
           reset after the test is complete
        """
        tmp_archive_dir = sami2py.archive_dir

        from sami2py import test_data_dir
        sami2py.utils.set_archive_dir(path=test_data_dir)

        with open(sami2py.archive_path, 'r') as archive_file:
            archive_dir = archive_file.readline()
        assert archive_dir == test_data_dir

        if os.path.isdir(tmp_archive_dir):
            sami2py.utils.set_archive_dir(path=tmp_archive_dir)
        else:
            with open(sami2py.archive_path, 'w') as archive_file:
                archive_file.write('')
                sami2py.archive_dir = ''

    @raises(ValueError)
    def test_set_archive_dir_exception(self):
        """if the provided path is invalid a value error should be produced
        """
        sami2py.utils.set_archive_dir('dummy_invalid_path')
