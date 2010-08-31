; Create test IDL save files. To run:
; idl < make_test_files.pro

; =========== SCALARS =========== 

; The types are listed here in the order of the IDL data type code

; 1 - byte

i8u = byte(234)

save, i8u, filename='data/scalar_byte.sav'

; 2 - 16-bit integers

i16s = -23456s

save, i16s, filename='data/scalar_int16.sav'

; 3 - 32-bit long integer

i32s = long(-1234567890)

save, i32s, filename='data/scalar_int32.sav'

; 4 - 32-bit floating point number

f32 = -3.1234567e+37

save, f32, filename='data/scalar_float32.sav'

; 5 - 64-bit floating point number

f64 = -1.1976931348623157d+307

save, f64, filename='data/scalar_float64.sav'

; 6 - complex 32-bit floating point number

c32 = complex(3.124442e13,-2.312442e31)

save, c32, filename='data/scalar_complex32.sav'

; 7 - string

s = "The quick brown fox jumps over the lazy python"

save, s, filename='data/scalar_string.sav'

; 8 - structure

; tested in the STRUCTURES section

; 9 - complex 64-bit floating point number

c64 = dcomplex(1.1987253647623157d+112,-5.1987258887729157d+307)

save, c64, filename='data/scalar_complex64.sav'

; 10 - heap pointer

c64_pointer1 = ptr_new(c64)
c64_pointer2 = c64_pointer1

save, c64_pointer1, c64_pointer2, filename='data/scalar_heap_pointer.sav'

; 12 - 16-bit unsigned integer

i16u = uint(65511)

save, i16u, filename='data/scalar_uint16.sav'

; 13 - 32-bit unsigned integer

i32u = ulong(4294967233)

save, i32u, filename='data/scalar_uint32.sav'

; 14 - 64-bit signed integer

i64s = long64(-9223372036854774567)

save, i64s, filename='data/scalar_int64.sav'

; 15 - 64-bit unsigned integer

i64u = ulong64(18446744073709529285)

save, i64u, filename='data/scalar_uint64.sav'

; =========== ARRAYS =========== 

array1d = fltarr(123)
save, array1d, filename='data/array_float32_1d.sav'

array2d = fltarr(12,22)
save, array2d, filename='data/array_float32_2d.sav'

array3d = fltarr(12,22,11)
save, array3d, filename='data/array_float32_3d.sav'

array4d = fltarr(7,8,5,4)
save, array4d, filename='data/array_float32_4d.sav'

array5d = fltarr(5,6,4,3,4)
save, array5d, filename='data/array_float32_5d.sav'

array6d = fltarr(4,3,5,4,6,3)
save, array6d, filename='data/array_float32_6d.sav'

array7d = fltarr(2,3,4,3,2,1,2)
save, array7d, filename='data/array_float32_7d.sav'

array8d = fltarr(4,5,3,2,1,2,3,4)
save, array8d, filename='data/array_float32_8d.sav'

; =========== STRUCTURES ===========

scalars = {a:1,b:2L,c:3.,d:4d,e:"spam",f:complex(-1.,3.)}
save,scalars,filename='data/struct_scalars.sav'

scalars_rep = replicate(scalars, 5)
save,scalars_rep,filename='data/struct_scalars_replicated.sav'

arrays = {a:[1,2,3],b:[4.,5.,6.,7.],c:[complex(1.,2.),complex(7.,8.)], d:["cheese","bacon","spam"]}
save,arrays,filename='data/struct_arrays.sav'

arrays_rep = replicate(arrays, 5)
save,arrays_rep,filename='data/struct_arrays_replicated.sav'

c = { circle, x:1, y:2, r:3 }  
fc = { filled_circle, c:4, INHERITS circle }  
save,fc,filename='data/struct_inherit.sav'

; =========== COMPRESSION ===========

save, i8u, f32, c64, array5d, arrays, filename='data/various_compressed.sav', /compress
