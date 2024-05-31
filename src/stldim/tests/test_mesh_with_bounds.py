"""
Test the MeshWithBounds class
"""

import pytest
import stldim

def test_3dbenchy():
    """
    Calculate the dimmensions of the 3DBenchy model and compare them to known values.
    """
    stl_dimensions = stldim.MeshWithBounds.from_file("tests/3DBenchy.stl")

    assert pytest.approx(stl_dimensions.minx) == -29.176
    assert pytest.approx(stl_dimensions.maxx) == 30.825
    assert pytest.approx(stl_dimensions.miny) == -15.502
    assert pytest.approx(stl_dimensions.maxy) == 15.502
    assert pytest.approx(stl_dimensions.minz) == 0.0
    assert pytest.approx(stl_dimensions.maxz) == 48.0

def test_filename():
    """
    Test the filename property
    """
    stl_dimensions = stldim.MeshWithBounds.from_file("tests/3DBenchy.stl")

    assert stl_dimensions.filename == "tests/3DBenchy.stl"

def test_sanitized_filename_plain():
    """
    Test the sanitized_filename property
    """
    stl_dimensions = stldim.MeshWithBounds.from_file("tests/test.stl")

    assert stl_dimensions.sanitized_filename == "test_stl"

def test_spaces():
    """
    Test with spaces in the filename
    """
    stl_dimensions = stldim.MeshWithBounds.from_file("tests/test test.stl")

    assert stl_dimensions.sanitized_filename == "test_test_stl"

def test_special_chars():
    """
    Test with special characters in the filename
    """
    stl_dimensions = stldim.MeshWithBounds.from_file("tests/test!@#$%^&*().stl")

    assert stl_dimensions.sanitized_filename == "test___________stl"

def test_leading_numbers():
    """
    Test with leading numbers in the filename
    """
    stl_dimensions = stldim.MeshWithBounds.from_file("tests/11test.stl")

    assert stl_dimensions.sanitized_filename == "__test_stl"

def test_trailing_numbers():
    """
    Test with trailing numbers in the filename
    """
    stl_dimensions = stldim.MeshWithBounds.from_file("tests/test11.stl")

    assert stl_dimensions.sanitized_filename == "test11_stl"

def test_no_extension():
    """
    Test with a filename with no extension
    """
    stl_dimensions = stldim.MeshWithBounds.from_file("tests/test")

    assert stl_dimensions.sanitized_filename == "test"

def test_subdirectory():
    """
    Test with a filename with a subdirectory
    """
    stl_dimensions = stldim.MeshWithBounds.from_file("tests/test.stl")

    assert stl_dimensions.sanitized_filename == "test_stl"

def test_empty_varname():
    """
    Test with an empty varnames
    """
    stl_dimensions = stldim.MeshWithBounds.from_file("tests/test.stl", varname="")

    assert stl_dimensions.varname == "test_stl"

def test_none_varname():
    """
    Test with varname set to None
    """
    stl_dimensions = stldim.MeshWithBounds.from_file("tests/test.stl", varname=None)

    assert stl_dimensions.varname == "test_stl"

def test_varname():
    """
    Test with a varname set
    """
    stl_dimensions = stldim.MeshWithBounds.from_file("tests/test.stl", varname="foobar")

    assert stl_dimensions.varname == "foobar"
