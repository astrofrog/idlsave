# IDLSave - a python module to read IDL 'save' files
# Copyright (c) 2010 Thomas P. Robitaille

# This code was developed by with permission from ITT Visual Information Systems.
# IDL(r) is a registered trademark of ITT Visual Information Systems, Inc. for
# their Interactive Data Language software.

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import struct
import numpy as np
import tempfile
import zlib
import warnings

dtype_dict = {}
dtype_dict[1] = '>u1'
dtype_dict[2] = '>i2'
dtype_dict[3] = '>i4'
dtype_dict[4] = '>f4'
dtype_dict[5] = '>f8'
dtype_dict[6] = '>c8'
dtype_dict[7] = '|O'
dtype_dict[8] = '|O'
dtype_dict[9] = '>c16'
dtype_dict[12] = '>u2'
dtype_dict[13] = '>u4'
dtype_dict[14] = '>i8'
dtype_dict[15] = '>u8'


def align_32(f):
    '''If not aligned with a 32-bit position, move to the next one'''
    pos = f.tell()
    if pos % 4 <> 0:
        f.seek(pos + 4 - pos % 4)


def skip_bytes(f, n):
    '''Skip `n` bytes'''
    f.read(n)
    return


def read_bytes(f, n):
    '''Read the next `n` bytes'''
    return f.read(n)


def read_byte(f):
    '''Read a single byte'''
    return np.uint8(struct.unpack('>B', f.read(4)[0])[0])


def read_long(f):
    '''Read a signed 32-bit integer'''
    return np.int32(struct.unpack('>l', f.read(4))[0])


def read_int16(f):
    '''Read a signed 16-bit integer'''
    return np.int16(struct.unpack('>h', f.read(4)[2:4])[0])


def read_int32(f):
    '''Read a signed 32-bit integer'''
    return np.int32(struct.unpack('>i', f.read(4))[0])


def read_int64(f):
    '''Read a signed 64-bit integer'''
    return np.int64(struct.unpack('>q', f.read(8))[0])


def read_uint16(f):
    '''Read an unsigned 16-bit integer'''
    return np.uint16(struct.unpack('>H', f.read(4)[2:4])[0])


def read_uint32(f):
    '''Read an unsigned 32-bit integer'''
    return np.uint32(struct.unpack('>I', f.read(4))[0])


def read_uint64(f):
    '''Read an unsigned 64-bit integer'''
    return np.uint64(struct.unpack('>Q', f.read(8))[0])


def read_float32(f):
    '''Read a 32-bit float'''
    return np.float32(struct.unpack('>f', f.read(4))[0])


def read_float64(f):
    '''Read a 64-bit float'''
    return np.float64(struct.unpack('>d', f.read(8))[0])


class Pointer(object):
    '''Class used to define pointers'''

    def __init__(self, index):
        self.index = index
        return

# Define the different record types that can be found in an IDL save file
rectype_dict = {}
rectype_dict[0] = "START_MARKER"
rectype_dict[1] = "COMMON_VARIABLE"
rectype_dict[2] = "VARIABLE"
rectype_dict[3] = "SYSTEM_VARIABLE"
rectype_dict[6] = "END_MARKER"
rectype_dict[10] = "TIMESTAMP"
rectype_dict[12] = "COMPILED"
rectype_dict[13] = "IDENTIFICATION"
rectype_dict[14] = "VERSION"
rectype_dict[15] = "HEAP_HEADER"
rectype_dict[16] = "HEAP_DATA"
rectype_dict[17] = "PROMOTE64"
rectype_dict[19] = "NOTICE"

# Define a dictionary to contain structure definitions
struct_dict = {}


def read_string(f):
    '''Read a string'''
    length = read_long(f)
    if length > 0:
        chars = read_bytes(f, length)
        align_32(f)
    else:
        chars = None
    return np.str(chars)


def read_string_data(f):
    '''Read a data string (length is specified twice)'''
    length = read_long(f)
    if length > 0:
        length = read_long(f)
        string = read_bytes(f, length)
        align_32(f)
    else:
        string = None
    return np.str(string)


def read_data(f, dtype):
    '''Read a variable with a specified data type'''
    if dtype==1:
        if read_int32(f) <> 1:
            raise Exception("Error occured while reading byte variable")
        return read_byte(f)
    elif dtype==2:
        return read_int16(f)
    elif dtype==3:
        return read_int32(f)
    elif dtype==4:
        return read_float32(f)
    elif dtype==5:
        return read_float64(f)
    elif dtype==6:
        real = read_float32(f)
        imag = read_float32(f)
        return np.complex64(real + imag * 1j)
    elif dtype==7:
        return read_string_data(f)
    elif dtype==8:
        raise Exception("Should not be here - please report this")
    elif dtype==9:
        real = read_float64(f)
        imag = read_float64(f)
        return np.complex128(real + imag * 1j)
    elif dtype==10:
        return Pointer(read_int32(f))
    elif dtype==11:
        raise Exception("Object reference type not implemented")
    elif dtype==12:
        return read_uint16(f)
    elif dtype==13:
        return read_uint32(f)
    elif dtype==14:
        return read_int64(f)
    elif dtype==15:
        return read_uint64(f)
    else:
        raise Exception("Unknown IDL type: %i - please report this" % dtype)


def read_structure(f, array_desc, struct_desc):
    '''
    Read a structure, with the array and structure descriptors given as
    `array_desc` and `structure_desc` respectively.
    '''

    nrows = array_desc.nelements
    ncols = struct_desc.ntags
    columns = struct_desc.tagtable

    dtype = []
    for col in columns:
        if col.structure or col.array:
            dtype.append(((col.name.lower(), col.name), np.object_))
        else:
            if col.typecode in dtype_dict:
                dtype.append(((col.name.lower(), col.name),
                                    dtype_dict[col.typecode]))
            else:
                raise Exception("Variable type %i not implemented" %
                                                            col.typecode)

    structure = np.recarray((nrows, ), dtype=dtype)

    for i in range(nrows):
        for col in columns:
            dtype = col.typecode
            if col.structure:
                structure[col.name][i] = read_structure(f, \
                                            struct_desc.arrtable[col.name], \
                                            struct_desc.structtable[col.name])
            elif col.array:
                structure[col.name][i] = read_array(f, dtype, \
                                            struct_desc.arrtable[col.name])
            else:
                structure[col.name][i] = read_data(f, dtype)

    return structure


def read_array(f, typecode, array_desc):
    '''
    Read an array of type `typecode`, with the array descriptor given as
    `array_desc`.
    '''

    if typecode in [1, 3, 4, 5, 6, 9, 13, 14, 15]:

        if typecode == 1:
            nbytes = read_int32(f)
            if nbytes <> array_desc.nbytes:
                raise Exception("Error occured while reading byte array")

        # Read bytes as numpy array
        array = np.fromstring(f.read(array_desc.nbytes), \
                                dtype=dtype_dict[typecode])

    elif typecode in [2, 12]:

        # These are 2 byte types, need to skip every two as they are not packed

        array = np.fromstring(f.read(array_desc.nbytes*2), \
                                dtype=dtype_dict[typecode])[1::2]

    else:

        # Read bytes into list
        array = []
        for i in range(array_desc.nelements):
            dtype = typecode
            data = read_data(f, dtype)
            array.append(data)

        array = np.array(array, dtype=np.object_)

    # Reshape array if needed
    if array_desc.ndims > 1:
        dims = array_desc.dims[:array_desc.ndims]
        dims.reverse()
        array = array.reshape(dims)

    # Go to next alignment position
    align_32(f)

    return array


class Record(object):
    '''Class for reading and storing complete records'''

    def __init__(self):
        self.end = False
        pass

    def read(self, f):

        self.recpos = f.tell()
        self.rectype = read_long(f)

        self.nextrec = read_uint32(f)
        self.nextrec += read_uint32(f) * 2**32

        skip_bytes(f, 4)

        if not self.rectype in rectype_dict:
            raise Exception("Unknown RECTYPE: %i" % self.rectype)

        self.rectype = rectype_dict[self.rectype]

        if self.rectype in ["VARIABLE", "HEAP_DATA"]:

            if self.rectype == "VARIABLE":
                self.varname = read_string(f)
            else:
                self.heap_index = read_long(f)
                skip_bytes(f, 4)

            self.rectypedesc = TypeDesc().read(f)

            varstart = read_long(f)
            if varstart <> 7:
                raise Exception("VARSTART is not 7")

            if self.rectypedesc.structure:
                self.data = read_structure(f, self.rectypedesc.array_desc, \
                                            self.rectypedesc.struct_desc)
            elif self.rectypedesc.array:
                self.data = read_array(f, self.rectypedesc.typecode, \
                                            self.rectypedesc.array_desc)
            else:
                dtype = self.rectypedesc.typecode
                self.data = read_data(f, dtype)

        elif self.rectype == "TIMESTAMP":

            skip_bytes(f, 4*256)
            self.date = read_string(f)
            self.user = read_string(f)
            self.host = read_string(f)

        elif self.rectype == "VERSION":

            self.format = read_long(f)
            self.arch = read_string(f)
            self.os = read_string(f)
            self.release = read_string(f)

        elif self.rectype == "IDENTIFICATON":

            self.author = read_string(f)
            self.title = read_string(f)
            self.idcode = read_string(f)

        elif self.rectype == "NOTICE":

            self.notice = read_string(f)

        elif self.rectype == "HEAP_HEADER":

            self.nvalues = read_long(f)
            self.indices = []
            for i in range(self.nvalues):
                self.indices.append(read_long(f))

        elif self.rectype == "COMMONBLOCK":

            self.nvars = read_long(f)
            self.name = read_string(f)
            self.varnames = []
            for i in range(self.nvars):
                self.varnames.append(read_string(f))

        elif self.rectype == "END_MARKER":

            self.end = True

        elif self.rectype == "UNKNOWN":

            print "Skipping UNKNOWN record"

        elif self.rectype == "SYSTEM_VARIABLE":

            print "Skipping SYSTEM_VARIABLE record"

        else:

            raise Exception("RECTYPE=%s not implemented" % self.rectype)

        f.seek(self.nextrec)

        return self

    def __str__(self):

        string = ""

        if self.rectype == "VARIABLE":

            string += "Name: %s\n" % self.varname
            string += "Type: %i" % self.typedesc.typecode

        elif self.rectype == "TIMESTAMP":

            string += "Date: %s\n" % self.date
            string += "User: %s\n" % self.user
            string += "Host: %s" % self.host

        elif self.rectype == "VERSION":

            string += "Format: %s\n" % self.format
            string += "Architecture: %s\n" % self.arch
            string += "Operating System: %s\n" % self.os
            string += "IDL Version: %s" % self.release

        elif self.rectype == "IDENTIFICATON":

            string += "Author: %s\n" % self.author
            string += "Title: %s\n" % self.title
            string += "ID Code: %s" % self.idcode

        elif self.rectype == "NOTICE":

            string += self.notice

        elif self.rectype == "HEAP_HEADER":

            string += "todo"

        elif self.rectype == "COMMONBLOCK":

            string += "todo"

        return string

    def __repr__(self):
        return "<IDL " + self.rectype + " object>"


class TypeDesc(object):
    '''Class for reading and storing data type descriptors'''

    def __init__(self):
        pass

    def read(self, f):

        self.typecode = read_long(f)
        self.varflags = read_long(f)

        if self.varflags & 2 == 2:
            raise Exception("System variables not implemented")

        self.array = self.varflags & 4 == 4
        self.structure = self.varflags & 32 == 32

        # CHECK VARFLAGS HERE TO SEE IF ARRAY

        if self.structure:
            self.array_desc = ArrayDesc().read(f)
            self.struct_desc = StructDesc().read(f)
        elif self.array:
            self.array_desc = ArrayDesc().read(f)

        return self


class ArrayDesc(object):
    '''Class for reading and storing array descriptors'''

    def __init__(self):
        pass

    def read(self, f):

        self.arrstart = read_long(f)

        if self.arrstart == 8:

            skip_bytes(f, 4)

            self.nbytes = read_long(f)
            self.nelements = read_long(f)
            self.ndims = read_long(f)

            skip_bytes(f, 8)

            self.nmax = read_long(f)

            self.dims = []
            for d in range(self.nmax):
                self.dims.append(read_long(f))

        elif self.arrstart == 18:

            warnings.warn("Using experimental 64-bit array read")

            skip_bytes(f, 8)

            self.nbytes = read_uint64(f)
            self.nelements = read_uint64(f)
            self.ndims = read_long(f)

            skip_bytes(f, 8)

            self.nmax = 8

            self.dims = []
            for d in range(self.nmax):
                v = read_long(f)
                if v <> 0:
                    raise Exception("Expected a zero in ARRAY_DESC")
                self.dims.append(read_long(f))

        else:

            raise Exception("Unknown ARRSTART: %i" % self.arrstart)

        return self


class StructDesc(object):
    '''Class for reading and storing structure descriptors'''

    def __init__(self):
        pass

    def read(self, f):

        structstart = read_long(f)
        if structstart <> 9:
            raise Exception("STRUCTSTART should be 9")

        self.name = read_string(f)
        self.predef = read_long(f)
        self.ntags = read_long(f)
        self.nbytes = read_long(f)

        if self.predef & 1 == 0:

            self.tagtable = []
            for t in range(self.ntags):
                self.tagtable.append(TagDesc().read(f))

            for i in range(self.ntags):
                self.tagtable[i].name = read_string(f)

            self.arrtable = {}
            for t in self.tagtable:
                if t.array:
                    self.arrtable[t.name] = ArrayDesc().read(f)

            self.structtable = {}
            for t in self.tagtable:
                if t.structure:
                    self.structtable[t.name] = StructDesc().read(f)

            struct_dict[self.name] = (self.tagtable, \
                                        self.arrtable, self.structtable)

        else:

            if not self.name in struct_dict:
                raise Exception("PREDEF=1 but can't find definition")

            self.tagtable, self.arrtable, self.structtable = \
                                                        struct_dict[self.name]

        return self


class TagDesc(object):
    '''Class for reading and storing tag descriptors'''

    def __init__(self):
        pass

    def read(self, f):

        self.offset = read_long(f)

        if self.offset == -1:
            self.offset = read_uint64(f)

        self.typecode = read_long(f)
        tagflags = read_long(f)

        self.array = tagflags & 4 == 4
        self.structure = tagflags & 32 == 32
        self.scalar = self.typecode in dtype_dict
        # Assume '10'x is scalar

        return self


class AttrDict(dict):
    '''
    A case-insensitive dictionary with access via item, attribute, and call notations:

        >>> d = AttrDict()
        >>> d['Variable'] = 123
        >>> d['Variable']
        123
        >>> d.Variable
        123
        >>> d.variable
        123
        >>> d('VARIABLE')
        123
    '''

    def __init__(self, init={}):
        dict.__init__(self, init)

    def __getitem__(self, name):
        return super(AttrDict, self).__getitem__(name.lower())

    def __setitem__(self, key, value):
        return super(AttrDict, self).__setitem__(key.lower(), value)

    __getattr__ = __getitem__
    __setattr__ = __setitem__
    __call__ = __getitem__


def read(file_name, idict=None, python_dict=False, uncompressed_file_name=None, verbose=True):
    '''
    Read an IDL .sav file

    Parameters
    ----------
    file_name : str
        Name of the IDL save file.
    idict : dict, optional
        Dictionary in which to insert .sav file variables
    python_dict: bool, optional
        By default, the object return is not a Python dictionary, but a
        case-insensitive dictionary with item, attribute, and call access
        to variables. To get a standard Python dictionary, set this option
        to True. If `idict` is specified, `attribute_access` is ignored.
    uncompressed_file_name : str, optional
        This option only has an effect for .sav files written with the
        /compress option. If a file name is specified, compressed .sav
        files are uncompressed to this file. Otherwise, idlsave will use
        the `tempfile` module to determine a temporary filename
        automatically, and will remove the temporary file upon successfully
        reading it in.
    verbose : bool, optional
        Whether to print out information about the save file, including
        the records read, and available variables.

    Returns
    ----------
    idl_dict : AttrDict or dict
        If `python_dict` is set to False (default), this function returns a
        case-insensitive dictionary with item, attribute, and call access
        to variables. If `python_dict` is set to True, this function
        returns a Python dictionary with all variable names in lowercase.
        If `idict` was specified, then variables are written to the
        dictionary specified, and the updated dictionary is returned.
    '''

    # Initialize record and variable holders
    records = []
    if python_dict or idict:
        variables = {}
    else:
        variables = AttrDict()

    # Open the IDL file
    f = file(file_name, 'rb')

    # Read the signature, which should be 'SR'
    signature = read_bytes(f, 2)
    if signature <> 'SR':
        raise Exception("Invalid SIGNATURE: %s" % signature)

    # Next, the record format, which is '\x00\x04' for normal .sav
    # files, and '\x00\x06' for compressed .sav files.
    recfmt = read_bytes(f, 2)

    if recfmt == '\x00\x04':
        pass

    elif recfmt == '\x00\x06':

        if verbose:
            print "IDL Save file is compressed"

        if uncompressed_file_name:
            fout = file(uncompressed_file_name, 'w+b')
        else:
            fout = tempfile.NamedTemporaryFile(suffix='.sav')

        if verbose:
            print " -> expanding to %s" % fout.name

        # Write header
        fout.write('SR\x00\x04')

        # Cycle through records
        while True:

            # Read record type
            rectype = read_long(f)
            fout.write(struct.pack('>l', rectype))

            # Read position of next record and return as int
            nextrec = read_uint32(f)
            nextrec += read_uint32(f) * 2**32

            # Read the unknown 4 bytes
            unknown = f.read(4)

            # Check if the end of the file has been reached
            if rectype_dict[rectype] == 'END_MARKER':
                fout.write(struct.pack('>I', int(nextrec) % 2**32))
                fout.write(struct.pack('>I', int((nextrec - (nextrec % 2**32)) / 2**32)))
                fout.write(unknown)
                break

            # Find current position
            pos = f.tell()

            # Decompress record
            string = zlib.decompress(f.read(nextrec-pos))

            # Find new position of next record
            nextrec = fout.tell() + len(string) + 12

            # Write out record
            fout.write(struct.pack('>I', int(nextrec % 2**32)))
            fout.write(struct.pack('>I', int((nextrec - (nextrec % 2**32)) / 2**32)))
            fout.write(unknown)
            fout.write(string)

        # Close the original compressed file
        f.close()

        # Set f to be the decompressed file, and skip the first four bytes
        f = fout
        f.seek(4)

    else:
        raise Exception("Invalid RECFMT: %s" % recfmt)

    # Loop through records, and add them to the list
    while True:
        r = Record().read(f)
        records.append(r)
        if r.end:
            break

    # Close the file
    f.close()

    # Find heap data variables
    heap = {}
    for r in records:
        if r.rectype == "HEAP_DATA":
            heap[r.heap_index] = r.data

    # Find all variables
    for r in records:
        if r.rectype == "VARIABLE":
            while isinstance(r.data, Pointer):
                r.data = heap[r.data.index]
            variables[r.varname.lower()] = r.data

    if verbose:

        # Create convenience list of record types
        rectypes = [r.rectype for r in records]

        for header in ['TIMESTAMP', 'VERSION', 'IDENTIFICATION']:
            if header in rectypes:
                print "-"*50
                pos = rectypes.index(header)
                print records[pos]

        print "-"*50
        print "Successfully read %i records of which:" % \
                                            (len(records))
        for rt in set(rectypes):
            if rt <> 'END_MARKER':
                print " - %i are of type %s" % (rectypes.count(rt), rt)
        print "-"*50

        if 'VARIABLE' in rectypes:
            print "Available variables:"
            for var in variables:
                print " - %s [%s]" % (var, type(variables[var]))
            print "-"*50

    if idict:
        for var in variables:
            idict[var] = variables[var]
        return idict
    else:
        return variables
