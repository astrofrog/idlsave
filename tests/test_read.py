import numpy as np
from numpy.testing import *

import idlsave


def object_array(*args):
    array = np.empty(len(args), dtype=np.object)
    for i in range(len(args)):
        array[i] = args[i]
    return array


def assert_identical(a, b):
    '''Assert whether value AND type are the same'''
    assert_equal(a, b)
    if type(b) is np.str:
        assert_equal(type(a), type(b))
    else:
        assert_equal(a.dtype.type, b.dtype.type)


def assert_array_identical(a, b):
    '''Assert whether values AND type are the same'''
    assert_array_equal(a, b)
    assert_equal(a.dtype.type, b.dtype.type)


class TestIdict:

    def test_idict(self):
        custom_dict = {'a':np.int16(999)}
        original_id = id(custom_dict)
        s = idlsave.read('data/scalar_byte.sav', idict=custom_dict, verbose=False)
        assert original_id, id(s)
        assert 'a' in s
        assert_identical(s['a'], np.int16(999))
        assert_identical(s['i8u'], np.uint8(234))


class TestScalars:

    def test_byte(self):
        s = idlsave.read('data/scalar_byte.sav', verbose=False)
        assert_identical(s.i8u, np.uint8(234))

    def test_int16(self):
        s = idlsave.read('data/scalar_int16.sav', verbose=False)
        assert_identical(s.i16s, np.int16(-23456))

    def test_int32(self):
        s = idlsave.read('data/scalar_int32.sav', verbose=False)
        assert_identical(s.i32s, np.int32(-1234567890))

    def test_float32(self):
        s = idlsave.read('data/scalar_float32.sav', verbose=False)
        assert_identical(s.f32, np.float32(-3.1234567e+37))

    def test_float64(self):
        s = idlsave.read('data/scalar_float64.sav', verbose=False)
        assert_identical(s.f64, np.float64(-1.1976931348623157e+307))

    def test_complex32(self):
        s = idlsave.read('data/scalar_complex32.sav', verbose=False)
        assert_identical(s.c32, np.complex64(3.124442e13-2.312442e31j))

    def test_string(self):
        s = idlsave.read('data/scalar_string.sav', verbose=False)
        assert_identical(s.s, np.str("The quick brown fox jumps over the lazy python"))

    def test_structure(self):
        pass

    def test_complex64(self):
        s = idlsave.read('data/scalar_complex64.sav', verbose=False)
        assert_identical(s.c64, np.complex128(1.1987253647623157e+112-5.1987258887729157e+307j))

    def test_heap_pointer(self):
        pass

    def test_object_reference(self):
        pass

    def test_uint16(self):
        s = idlsave.read('data/scalar_uint16.sav', verbose=False)
        assert_identical(s.i16u, np.uint16(65511))

    def test_uint32(self):
        s = idlsave.read('data/scalar_uint32.sav', verbose=False)
        assert_identical(s.i32u, np.uint32(4294967233))

    def test_int64(self):
        s = idlsave.read('data/scalar_int64.sav', verbose=False)
        assert_identical(s.i64s, np.int64(-9223372036854774567))

    def test_uint64(self):
        s = idlsave.read('data/scalar_uint64.sav', verbose=False)
        assert_identical(s.i64u, np.uint64(18446744073709529285))


class TestCompressed(TestScalars):

    def test_compressed(self):
        s = idlsave.read('data/various_compressed.sav', verbose=False)
        assert_identical(s.i8u, np.uint8(234))
        assert_identical(s.f32, np.float32(-3.1234567e+37))
        assert_identical(s.c64, np.complex128(1.1987253647623157e+112-5.1987258887729157e+307j))
        assert s.array5d.shape == (4, 3, 4, 6, 5)
        assert_identical(s.arrays.a[0], np.array([1, 2, 3], dtype=np.int16))
        assert_identical(s.arrays.b[0], np.array([4., 5., 6., 7.], dtype=np.float32))
        assert_identical(s.arrays.c[0], np.array([np.complex64(1+2j), np.complex64(7+8j)]))
        assert_identical(s.arrays.d[0], np.array(["cheese", "bacon", "spam"], dtype=np.object))


class TestArrayDimensions:

    def test_1d(self):
        s = idlsave.read('data/array_float32_1d.sav', verbose=False)
        assert s.array1d.shape == (123, )

    def test_2d(self):
        s = idlsave.read('data/array_float32_2d.sav', verbose=False)
        print s.array2d.shape
        assert s.array2d.shape == (22, 12)

    def test_3d(self):
        s = idlsave.read('data/array_float32_3d.sav', verbose=False)
        assert s.array3d.shape == (11, 22, 12)

    def test_4d(self):
        s = idlsave.read('data/array_float32_4d.sav', verbose=False)
        assert s.array4d.shape == (4, 5, 8, 7)

    def test_5d(self):
        s = idlsave.read('data/array_float32_5d.sav', verbose=False)
        assert s.array5d.shape == (4, 3, 4, 6, 5)

    def test_6d(self):
        s = idlsave.read('data/array_float32_6d.sav', verbose=False)
        assert s.array6d.shape == (3, 6, 4, 5, 3, 4)

    def test_7d(self):
        s = idlsave.read('data/array_float32_7d.sav', verbose=False)
        assert s.array7d.shape == (2, 1, 2, 3, 4, 3, 2)

    def test_8d(self):
        s = idlsave.read('data/array_float32_8d.sav', verbose=False)
        assert s.array8d.shape == (4, 3, 2, 1, 2, 3, 5, 4)


class TestStructures:

    def test_scalars(self):
        s = idlsave.read('data/struct_scalars.sav', verbose=False)
        assert_identical(s.scalars.a, np.array(np.int16(1)))
        assert_identical(s.scalars.b, np.array(np.int32(2)))
        assert_identical(s.scalars.c, np.array(np.float32(3.)))
        assert_identical(s.scalars.d, np.array(np.float64(4.)))
        assert_identical(s.scalars.e, np.array(["spam"], dtype=np.object))
        assert_identical(s.scalars.f, np.array(np.complex64(-1.+3j)))

    def test_scalars_replicated(self):
        s = idlsave.read('data/struct_scalars_replicated.sav', verbose=False)
        assert_identical(s.scalars_rep.a, np.repeat(np.int16(1), 5))
        assert_identical(s.scalars_rep.b, np.repeat(np.int32(2), 5))
        assert_identical(s.scalars_rep.c, np.repeat(np.float32(3.), 5))
        assert_identical(s.scalars_rep.d, np.repeat(np.float64(4.), 5))
        assert_identical(s.scalars_rep.e, np.repeat("spam", 5).astype(np.object))
        assert_identical(s.scalars_rep.f, np.repeat(np.complex64(-1.+3j), 5))

    def test_arrays(self):
        s = idlsave.read('data/struct_arrays.sav', verbose=False)
        assert_array_identical(s.arrays.a[0], np.array([1, 2, 3], dtype=np.int16))
        assert_array_identical(s.arrays.b[0], np.array([4., 5., 6., 7.], dtype=np.float32))
        assert_array_identical(s.arrays.c[0], np.array([np.complex64(1+2j), np.complex64(7+8j)]))
        assert_array_identical(s.arrays.d[0], np.array(["cheese", "bacon", "spam"], dtype=np.object))

    def test_arrays_replicated(self):

        s = idlsave.read('data/struct_arrays_replicated.sav', verbose=False)

        # Check column types
        assert s.arrays_rep.a.dtype.type is np.object_
        assert s.arrays_rep.b.dtype.type is np.object_
        assert s.arrays_rep.c.dtype.type is np.object_
        assert s.arrays_rep.d.dtype.type is np.object_

        # Check column shapes
        assert s.arrays_rep.a.shape == (5, )
        assert s.arrays_rep.b.shape == (5, )
        assert s.arrays_rep.c.shape == (5, )
        assert s.arrays_rep.d.shape == (5, )

        # Check values
        for i in range(5):
            assert_array_identical(s.arrays_rep.a[i], np.array([1, 2, 3], dtype=np.int16))
            assert_array_identical(s.arrays_rep.b[i], np.array([4., 5., 6., 7.], dtype=np.float32))
            assert_array_identical(s.arrays_rep.c[i], np.array([np.complex64(1+2j), np.complex64(7+8j)]))
            assert_array_identical(s.arrays_rep.d[i], np.array(["cheese", "bacon", "spam"], dtype=np.object))


class TestPointers:

    def test_pointers(self):
        s = idlsave.read('data/scalar_heap_pointer.sav', verbose=False)
        assert_identical(s.c64_pointer1, np.complex128(1.1987253647623157e+112-5.1987258887729157e+307j))
        assert_identical(s.c64_pointer2, np.complex128(1.1987253647623157e+112-5.1987258887729157e+307j))
        assert s.c64_pointer1 is s.c64_pointer2


if __name__ == "__main__":
    run_module_suite()
