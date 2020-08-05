#!/usr/bin/env python
#-*-Mode:python;coding:utf-8;tab-width:4;c-basic-offset:4;indent-tabs-mode:()-*-
# ex: set ft=python fenc=utf-8 sts=4 ts=4 sw=4 et nomod:
#
# MIT License
#
# Copyright (c) 2011-2019 Michael Truog <mjtruog at protonmail dot com>
#
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
#
"""
Erlang Binary Term Format Encoding/Decoding
"""

import sys
import struct
import zlib
import copy

def etfDictToJson(target_dictionary, etf_data):
    if etf_data is None or type(etf_data) is not dict:
        return
    for key in etf_data.keys():
        if type(key) == str:
            index = key
        else:
            index = key.value
        serialized_val = etf_data[key]
        if type(serialized_val) == dict:
            target_dictionary[index] = {}
            etfDictToJson(target_dictionary[index], serialized_val)
            continue
        if type(serialized_val) == list:
            target_dictionary[index] = []
            for serialized_list_entry in serialized_val:
                if type(serialized_list_entry) == dict:
                    target_dictionary[index].append({})
                    etfDictToJson(target_dictionary[index][-1], serialized_list_entry)
                if type(serialized_list_entry) == OtpErlangBinary:
                    target_dictionary[index].append(serialized_list_entry.value)
                else:
                    target_dictionary[index].append(serialized_list_entry)
            continue
        if type(serialized_val) in (OtpErlangAtom, OtpErlangBinary):
            target_dictionary[index] = serialized_val.value
        else:
            target_dictionary[index] = serialized_val

def getName(erlangKey):
    erlangKeyText = "%s" % erlangKey
    if type(erlangKey) == OtpErlangAtom:
        searchText = "OtpErlangAtom('"
        if erlangKeyText.find(searchText) != -1:
            return (erlangKeyText)[erlangKeyText.find(searchText)+len(searchText):len(erlangKeyText)-2]
    elif type(erlangKey) == OtpErlangBinary:
        searchText1 = "OtpErlangBinary('"
        searchText2 = "',bits="
        if erlangKeyText.find(searchText1) != -1:
            return (erlangKeyText)[erlangKeyText.find(searchText1)+len(searchText1):erlangKeyText.find(searchText2)]
    return erlangKey

if sys.version_info[0] >= 3:
    TypeLong = int
    TypeUnicode = str
    def b_chr(integer):
        """
        bytes chr function
        """
        return bytes([integer])
    def b_ord(character):
        """
        bytes ord function
        """
        return character
else:
    TypeLong = long
    TypeUnicode = unicode
    def b_chr(integer):
        """
        bytes chr function
        """
        return chr(integer)
    def b_ord(character):
        """
        bytes ord function
        """
        return ord(character)

__all__ = ['OtpErlangAtom',
           'OtpErlangBinary',
           'OtpErlangFunction',
           'OtpErlangList',
           'OtpErlangPid',
           'OtpErlangPort',
           'OtpErlangReference',
           'binary_to_term',
           'term_to_binary',
           'InputException',
           'OutputException',
           'ParseException']

# tag values here http://www.erlang.org/doc/apps/erts/erl_ext_dist.html
_TAG_VERSION = 131
_TAG_COMPRESSED_ZLIB = 80
_TAG_NEW_FLOAT_EXT = 70
_TAG_BIT_BINARY_EXT = 77
_TAG_ATOM_CACHE_REF = 78
_TAG_NEW_PID_EXT = 88
_TAG_NEW_PORT_EXT = 89
_TAG_NEWER_REFERENCE_EXT = 90
_TAG_SMALL_INTEGER_EXT = 97
_TAG_INTEGER_EXT = 98
_TAG_FLOAT_EXT = 99
_TAG_ATOM_EXT = 100
_TAG_REFERENCE_EXT = 101
_TAG_PORT_EXT = 102
_TAG_PID_EXT = 103
_TAG_SMALL_TUPLE_EXT = 104
_TAG_LARGE_TUPLE_EXT = 105
_TAG_NIL_EXT = 106
_TAG_STRING_EXT = 107
_TAG_LIST_EXT = 108
_TAG_BINARY_EXT = 109
_TAG_SMALL_BIG_EXT = 110
_TAG_LARGE_BIG_EXT = 111
_TAG_NEW_FUN_EXT = 112
_TAG_EXPORT_EXT = 113
_TAG_NEW_REFERENCE_EXT = 114
_TAG_SMALL_ATOM_EXT = 115
_TAG_MAP_EXT = 116
_TAG_FUN_EXT = 117
_TAG_ATOM_UTF8_EXT = 118
_TAG_SMALL_ATOM_UTF8_EXT = 119

# Erlang term classes listed alphabetically

class OtpErlangAtom(object):
    """
    OtpErlangAtom
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, value):
        self.value = value
    def binary(self):
        """
        return encoded representation
        """
        if isinstance(self.value, int):
            return b_chr(_TAG_ATOM_CACHE_REF) + b_chr(self.value)
        elif isinstance(self.value, TypeUnicode):
            value_encoded = self.value.encode('utf-8')
            length = len(value_encoded)
            if length <= 255:
                return (
                    b_chr(_TAG_SMALL_ATOM_UTF8_EXT) +
                    b_chr(length) + value_encoded
                )
            elif length <= 65535:
                return (
                    b_chr(_TAG_ATOM_UTF8_EXT) +
                    struct.pack(b'>H', length) + value_encoded
                )
            else:
                raise OutputException('uint16 overflow')
        elif isinstance(self.value, bytes):
            length = len(self.value)
            if length <= 255:
                return b_chr(_TAG_SMALL_ATOM_EXT) + b_chr(length) + self.value
            elif length <= 65535:
                return (
                    b_chr(_TAG_ATOM_EXT) +
                    struct.pack(b'>H', length) + self.value
                )
            else:
                raise OutputException('uint16 overflow')
        else:
            raise OutputException('unknown atom type')
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.value))
    def __hash__(self):
        return hash(self.binary())
    def __eq__(self, other):
        return self.binary() == other.binary()

class OtpErlangBinary(object):
    """
    OtpErlangBinary
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, value, bits=8):
        self.value = value
        self.bits = bits # bits in last byte
    def binary(self):
        """
        return encoded representation
        """
        if isinstance(self.value, bytes):
            length = len(self.value)
            if length > 4294967295:
                raise OutputException('uint32 overflow')
            elif self.bits != 8:
                return (
                    b_chr(_TAG_BIT_BINARY_EXT) +
                    struct.pack(b'>I', length) +
                    b_chr(self.bits) + self.value
                )
            else:
                return (
                    b_chr(_TAG_BINARY_EXT) +
                    struct.pack(b'>I', length) +
                    self.value
                )
        else:
            raise OutputException('unknown binary type')
    def __repr__(self):
        return '%s(%s,bits=%s)' % (
            self.__class__.__name__, repr(self.value), repr(self.bits)
        )
    def __hash__(self):
        return hash(self.binary())
    def __eq__(self, other):
        return self.binary() == other.binary()

class OtpErlangFunction(object):
    """
    OtpErlangFunction
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value
    def binary(self):
        """
        return encoded representation
        """
        return b_chr(self.tag) + self.value
    def __repr__(self):
        return '%s(%s,%s)' % (
            self.__class__.__name__,
            repr(self.tag), repr(self.value)
        )
    def __hash__(self):
        return hash(self.binary())
    def __eq__(self, other):
        return self.binary() == other.binary()

class OtpErlangList(object):
    """
    OtpErlangList
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, value, improper=False):
        self.value = value
        self.improper = improper # no empty list tail?
    def binary(self):
        """
        return encoded representation
        """
        if isinstance(self.value, list):
            length = len(self.value)
            if length == 0:
                return b_chr(_TAG_NIL_EXT)
            elif length > 4294967295:
                raise OutputException('uint32 overflow')
            elif self.improper:
                return (
                    b_chr(_TAG_LIST_EXT) +
                    struct.pack(b'>I', length - 1) +
                    b''.join([_term_to_binary(element)
                              for element in self.value])
                )
            else:
                return (
                    b_chr(_TAG_LIST_EXT) +
                    struct.pack(b'>I', length) +
                    b''.join([_term_to_binary(element)
                              for element in self.value]) +
                    b_chr(_TAG_NIL_EXT)
                )
        else:
            raise OutputException('unknown list type')
    def __repr__(self):
        return '%s(%s,improper=%s)' % (
            self.__class__.__name__, repr(self.value), repr(self.improper)
        )
    def __hash__(self):
        return hash(self.binary())
    def __eq__(self, other):
        return self.binary() == other.binary()

class OtpErlangPid(object):
    """
    OtpErlangPid
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, node, id_value, serial, creation):
        # pylint: disable=invalid-name
        self.node = node
        self.id = id_value
        self.serial = serial
        self.creation = creation
    def binary(self):
        """
        return encoded representation
        """
        creation_size = len(self.creation)
        if creation_size == 1:
            return (
                b_chr(_TAG_PID_EXT) +
                self.node.binary() + self.id + self.serial + self.creation
            )
        elif creation_size == 4:
            return (
                b_chr(_TAG_NEW_PID_EXT) +
                self.node.binary() + self.id + self.serial + self.creation
            )
        else:
            raise OutputException('unknown pid type')
    def __repr__(self):
        return '%s(%s,%s,%s,%s)' % (
            self.__class__.__name__,
            repr(self.node), repr(self.id), repr(self.serial),
            repr(self.creation)
        )
    def __hash__(self):
        return hash(self.binary())
    def __eq__(self, other):
        return self.binary() == other.binary()

class OtpErlangPort(object):
    """
    OtpErlangPort
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, node, id_value, creation):
        # pylint: disable=invalid-name
        self.node = node
        self.id = id_value
        self.creation = creation
    def binary(self):
        """
        return encoded representation
        """
        creation_size = len(self.creation)
        if creation_size == 1:
            return (
                b_chr(_TAG_PORT_EXT) +
                self.node.binary() + self.id + self.creation
            )
        elif creation_size == 4:
            return (
                b_chr(_TAG_NEW_PORT_EXT) +
                self.node.binary() + self.id + self.creation
            )
        else:
            raise OutputException('unknown port type')
    def __repr__(self):
        return '%s(%s,%s,%s)' % (
            self.__class__.__name__,
            repr(self.node), repr(self.id), repr(self.creation)
        )
    def __hash__(self):
        return hash(self.binary())
    def __eq__(self, other):
        return self.binary() == other.binary()

class OtpErlangReference(object):
    """
    OtpErlangReference
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, node, id_value, creation):
        # pylint: disable=invalid-name
        self.node = node
        self.id = id_value
        self.creation = creation
    def binary(self):
        """
        return encoded representation
        """
        length = int(len(self.id) / 4)
        if length == 0:
            return (
                b_chr(_TAG_REFERENCE_EXT) +
                self.node.binary() + self.id + self.creation
            )
        elif length <= 65535:
            creation_size = len(self.creation)
            if creation_size == 1:
                return (
                    b_chr(_TAG_NEW_REFERENCE_EXT) +
                    struct.pack(b'>H', length) +
                    self.node.binary() + self.creation + self.id
                )
            elif creation_size == 4:
                return (
                    b_chr(_TAG_NEWER_REFERENCE_EXT) +
                    struct.pack(b'>H', length) +
                    self.node.binary() + self.creation + self.id
                )
            else:
                raise OutputException('unknown reference type')
        else:
            raise OutputException('uint16 overflow')
    def __repr__(self):
        return '%s(%s,%s,%s)' % (
            self.__class__.__name__,
            repr(self.node), repr(self.id), repr(self.creation)
        )
    def __hash__(self):
        return hash(self.binary())
    def __eq__(self, other):
        return self.binary() == other.binary()

# dependency to support Erlang maps as map keys in python

class frozendict(dict):
    """
    frozendict is under the PSF (Python Software Foundation) License
    (from http://code.activestate.com/recipes/414283-frozen-dictionaries/)
    """
    # pylint: disable=invalid-name
    def _blocked_attribute(self):
        # pylint: disable=no-self-use
        raise AttributeError('A frozendict cannot be modified.')
    _blocked_attribute = property(_blocked_attribute)
    __delitem__ = __setitem__ = clear = _blocked_attribute
    pop = popitem = setdefault = update = _blocked_attribute
    def __new__(cls, *args, **kw):
        # pylint: disable=unused-argument
        # pylint: disable=too-many-nested-blocks
        new = dict.__new__(cls)
        args_ = []
        for arg in args:
            if isinstance(arg, dict):
                arg = copy.copy(arg)
                for k, v in arg.items():
                    if isinstance(v, dict):
                        arg[k] = frozendict(v)
                    elif isinstance(v, list):
                        v_ = list()
                        for elm in v:
                            if isinstance(elm, dict):
                                v_.append(frozendict(elm))
                            else:
                                v_.append(elm)
                        arg[k] = tuple(v_)
                args_.append(arg)
            else:
                args_.append(arg)
        dict.__init__(new, *args_, **kw)
        return new
    def __init__(self, *args, **kw):
        # pylint: disable=unused-argument
        # pylint: disable=super-init-not-called
        self.__cached_hash = None
    def __hash__(self):
        if self.__cached_hash is None:
            self.__cached_hash = hash(frozenset(self.items()))
        return self.__cached_hash
    def __repr__(self):
        return "frozendict(%s)" % dict.__repr__(self)

# core functionality

def binary_to_term(data):
    """
    Decode Erlang terms within binary data into Python types
    """
    if not isinstance(data, bytes):
        raise ParseException('not bytes input')
    size = len(data)
    if size <= 1:
        raise ParseException('null input')
    if b_ord(data[0]) != _TAG_VERSION:
        raise ParseException('invalid version')
    try:
        i, term = _binary_to_term(1, data)
        if i != size:
            raise ParseException('unparsed data')
        return term
    except struct.error:
        raise ParseException('missing data')
    except IndexError:
        raise ParseException('missing data')

def term_to_binary(term, compressed=False):
    """
    Encode Python types into Erlang terms in binary data
    """
    data_uncompressed = _term_to_binary(term)
    if compressed is False:
        return b_chr(_TAG_VERSION) + data_uncompressed
    else:
        if compressed is True:
            compressed = 6
        if compressed < 0 or compressed > 9:
            raise InputException('compressed in [0..9]')
        data_compressed = zlib.compress(data_uncompressed, compressed)
        size_uncompressed = len(data_uncompressed)
        if size_uncompressed > 4294967295:
            raise OutputException('uint32 overflow')
        return (
            b_chr(_TAG_VERSION) + b_chr(_TAG_COMPRESSED_ZLIB) +
            struct.pack(b'>I', size_uncompressed) + data_compressed
        )

# binary_to_term implementation functions

def _binary_to_term(i, data):
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    tag = b_ord(data[i])
    i += 1
    if tag == _TAG_NEW_FLOAT_EXT:
        return (i + 8, struct.unpack(b'>d', data[i:i + 8])[0])
    elif tag == _TAG_BIT_BINARY_EXT:
        j = struct.unpack(b'>I', data[i:i + 4])[0]
        i += 4
        bits = b_ord(data[i])
        i += 1
        return (i + j, OtpErlangBinary(data[i:i + j], bits))
    elif tag == _TAG_ATOM_CACHE_REF:
        return (i + 1, OtpErlangAtom(b_ord(data[i])))
    elif tag == _TAG_SMALL_INTEGER_EXT:
        return (i + 1, b_ord(data[i]))
    elif tag == _TAG_INTEGER_EXT:
        return (i + 4, struct.unpack(b'>i', data[i:i + 4])[0])
    elif tag == _TAG_FLOAT_EXT:
        value = float(data[i:i + 31].partition(b_chr(0))[0])
        return (i + 31, value)
    elif tag == _TAG_ATOM_EXT:
        j = struct.unpack(b'>H', data[i:i + 2])[0]
        i += 2
        return (i + j, OtpErlangAtom(data[i:i + j]))
    elif (tag == _TAG_NEW_PORT_EXT or
          tag == _TAG_REFERENCE_EXT or tag == _TAG_PORT_EXT):
        i, node = _binary_to_atom(i, data)
        id_value = data[i:i + 4]
        i += 4
        if tag == _TAG_NEW_PORT_EXT:
            creation = data[i:i + 4]
            i += 4
        else:
            creation = data[i:i + 1]
            i += 1
            if tag == _TAG_REFERENCE_EXT:
                return (i, OtpErlangReference(node, id_value, creation))
        # tag == _TAG_NEW_PORT_EXT or tag == _TAG_PORT_EXT
        return (i, OtpErlangPort(node, id_value, creation))
    elif tag == _TAG_NEW_PID_EXT or tag == _TAG_PID_EXT:
        i, node = _binary_to_atom(i, data)
        id_value = data[i:i + 4]
        i += 4
        serial = data[i:i + 4]
        i += 4
        if tag == _TAG_NEW_PID_EXT:
            creation = data[i:i + 4]
            i += 4
        elif tag == _TAG_PID_EXT:
            creation = data[i:i + 1]
            i += 1
        return (i, OtpErlangPid(node, id_value, serial, creation))
    elif tag == _TAG_SMALL_TUPLE_EXT or tag == _TAG_LARGE_TUPLE_EXT:
        if tag == _TAG_SMALL_TUPLE_EXT:
            length = b_ord(data[i])
            i += 1
        elif tag == _TAG_LARGE_TUPLE_EXT:
            length = struct.unpack(b'>I', data[i:i + 4])[0]
            i += 4
        i, tuple_value = _binary_to_term_sequence(i, length, data)
        return (i, tuple(tuple_value))
    elif tag == _TAG_NIL_EXT:
        return (i, [])
    elif tag == _TAG_STRING_EXT:
        j = struct.unpack(b'>H', data[i:i + 2])[0]
        i += 2
        return (i + j, data[i:i + j])
    elif tag == _TAG_LIST_EXT:
        length = struct.unpack(b'>I', data[i:i + 4])[0]
        i += 4
        i, list_value = _binary_to_term_sequence(i, length, data)
        i, tail = _binary_to_term(i, data)
        if not isinstance(tail, list) or tail != []:
            list_value.append(tail)
            list_value = OtpErlangList(list_value, improper=True)
        return (i, list_value)
    elif tag == _TAG_BINARY_EXT:
        j = struct.unpack(b'>I', data[i:i + 4])[0]
        i += 4
        return (i + j, OtpErlangBinary(data[i:i + j], 8))
    elif tag == _TAG_SMALL_BIG_EXT or tag == _TAG_LARGE_BIG_EXT:
        if tag == _TAG_SMALL_BIG_EXT:
            j = b_ord(data[i])
            i += 1
        elif tag == _TAG_LARGE_BIG_EXT:
            j = struct.unpack(b'>I', data[i:i + 4])[0]
            i += 4
        sign = b_ord(data[i])
        bignum = 0
        for bignum_index in range(j):
            digit = b_ord(data[i + j - bignum_index])
            bignum = bignum * 256 + int(digit)
        if sign == 1:
            bignum *= -1
        i += 1
        return (i + j, bignum)
    elif tag == _TAG_NEW_FUN_EXT:
        length = struct.unpack(b'>I', data[i:i + 4])[0]
        return (i + length, OtpErlangFunction(tag, data[i:i + length]))
    elif tag == _TAG_EXPORT_EXT:
        old_i = i
        i, _ = _binary_to_atom(i, data)
        i, _ = _binary_to_atom(i, data)
        if b_ord(data[i]) != _TAG_SMALL_INTEGER_EXT:
            raise ParseException('invalid small integer tag')
        i += 1
        _ = b_ord(data[i])
        i += 1
        return (i, OtpErlangFunction(tag, data[old_i:i]))
    elif tag == _TAG_NEWER_REFERENCE_EXT or tag == _TAG_NEW_REFERENCE_EXT:
        j = struct.unpack(b'>H', data[i:i + 2])[0] * 4
        i += 2
        i, node = _binary_to_atom(i, data)
        if tag == _TAG_NEWER_REFERENCE_EXT:
            creation = data[i:i + 4]
            i += 4
        elif tag == _TAG_NEW_REFERENCE_EXT:
            creation = data[i:i + 1]
            i += 1
        return (i + j, OtpErlangReference(node, data[i: i + j], creation))
    elif tag == _TAG_SMALL_ATOM_EXT:
        j = b_ord(data[i])
        i += 1
        atom_name = data[i:i + j]
        i = i + j
        if atom_name == b'true':
            return (i, True)
        elif atom_name == b'false':
            return (i, False)
        return (i, OtpErlangAtom(atom_name))
    elif tag == _TAG_MAP_EXT:
        length = struct.unpack(b'>I', data[i:i + 4])[0]
        i += 4
        pairs = {}
        for _ in range(length):
            i, key = _binary_to_term(i, data)
            i, value = _binary_to_term(i, data)
            if isinstance(key, dict):
                pairs[frozendict(key)] = value
            elif isinstance(key, list):
                pairs[OtpErlangList(key)] = value
            else:
                pairs[key] = value
        return (i, pairs)
    elif tag == _TAG_FUN_EXT:
        old_i = i
        numfree = struct.unpack(b'>I', data[i:i + 4])[0]
        i += 4
        i, _ = _binary_to_pid(i, data)
        i, _ = _binary_to_atom(i, data)
        i, _ = _binary_to_integer(i, data)
        i, _ = _binary_to_integer(i, data)
        i, _ = _binary_to_term_sequence(i, numfree, data)
        return (i, OtpErlangFunction(tag, data[old_i:i]))
    elif tag == _TAG_ATOM_UTF8_EXT:
        j = struct.unpack(b'>H', data[i:i + 2])[0]
        i += 2
        atom_name = TypeUnicode(
            data[i:i + j], encoding='utf-8', errors='strict'
        )
        return (i + j, OtpErlangAtom(atom_name))
    elif tag == _TAG_SMALL_ATOM_UTF8_EXT:
        j = b_ord(data[i])
        i += 1
        atom_name = TypeUnicode(
            data[i:i + j], encoding='utf-8', errors='strict'
        )
        return (i + j, OtpErlangAtom(atom_name))
    elif tag == _TAG_COMPRESSED_ZLIB:
        size_uncompressed = struct.unpack(b'>I', data[i:i + 4])[0]
        if size_uncompressed == 0:
            raise ParseException('compressed data null')
        i += 4
        data_compressed = data[i:]
        j = len(data_compressed)
        data_uncompressed = zlib.decompress(data_compressed)
        if size_uncompressed != len(data_uncompressed):
            raise ParseException('compression corrupt')
        (i_new, term) = _binary_to_term(0, data_uncompressed)
        if i_new != size_uncompressed:
            raise ParseException('unparsed data')
        return (i + j, term)
    else:
        raise ParseException('invalid tag')

def _binary_to_term_sequence(i, length, data):
    sequence = []
    for _ in range(length):
        i, element = _binary_to_term(i, data)
        sequence.append(element)
    return (i, sequence)

# (binary_to_term Erlang term primitive type functions)

def _binary_to_integer(i, data):
    tag = b_ord(data[i])
    i += 1
    if tag == _TAG_SMALL_INTEGER_EXT:
        return (i + 1, b_ord(data[i]))
    elif tag == _TAG_INTEGER_EXT:
        return (i + 4, struct.unpack(b'>i', data[i:i + 4])[0])
    else:
        raise ParseException('invalid integer tag')

def _binary_to_pid(i, data):
    tag = b_ord(data[i])
    i += 1
    if tag == _TAG_NEW_PID_EXT:
        i, node = _binary_to_atom(i, data)
        id_value = data[i:i + 4]
        i += 4
        serial = data[i:i + 4]
        i += 4
        creation = data[i:i + 4]
        i += 4
        return (i, OtpErlangPid(node, id_value, serial, creation))
    elif tag == _TAG_PID_EXT:
        i, node = _binary_to_atom(i, data)
        id_value = data[i:i + 4]
        i += 4
        serial = data[i:i + 4]
        i += 4
        creation = data[i:i + 1]
        i += 1
        return (i, OtpErlangPid(node, id_value, serial, creation))
    else:
        raise ParseException('invalid pid tag')

def _binary_to_atom(i, data):
    tag = b_ord(data[i])
    i += 1
    if tag == _TAG_ATOM_EXT:
        j = struct.unpack(b'>H', data[i:i + 2])[0]
        i += 2
        return (i + j, OtpErlangAtom(data[i:i + j]))
    elif tag == _TAG_ATOM_CACHE_REF:
        return (i + 1, OtpErlangAtom(b_ord(data[i])))
    elif tag == _TAG_SMALL_ATOM_EXT:
        j = b_ord(data[i])
        i += 1
        return (i + j, OtpErlangAtom(data[i:i + j]))
    elif tag == _TAG_ATOM_UTF8_EXT:
        j = struct.unpack(b'>H', data[i:i + 2])[0]
        i += 2
        atom_name = TypeUnicode(
            data[i:i + j], encoding='utf-8', errors='strict'
        )
        return (i + j, OtpErlangAtom(atom_name))
    elif tag == _TAG_SMALL_ATOM_UTF8_EXT:
        j = b_ord(data[i])
        i += 1
        atom_name = TypeUnicode(
            data[i:i + j], encoding='utf-8', errors='strict'
        )
        return (i + j, OtpErlangAtom(atom_name))
    else:
        raise ParseException('invalid atom tag')

# term_to_binary implementation functions

def _term_to_binary(term):
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    if isinstance(term, bytes):
        return _string_to_binary(term)
    elif isinstance(term, TypeUnicode):
        return _string_to_binary(
            term.encode(encoding='utf-8', errors='strict')
        )
    elif isinstance(term, list):
        return OtpErlangList(term).binary()
    elif isinstance(term, tuple):
        return _tuple_to_binary(term)
    elif isinstance(term, bool):
        return OtpErlangAtom(term and b'true' or b'false').binary()
    elif isinstance(term, (int, TypeLong)):
        return _long_to_binary(term)
    elif isinstance(term, float):
        return _float_to_binary(term)
    elif isinstance(term, dict):
        return _dict_to_binary(term)
    elif term is None:
        return OtpErlangAtom(b'undefined').binary()
    elif isinstance(term, OtpErlangAtom):
        return term.binary()
    elif isinstance(term, OtpErlangList):
        return term.binary()
    elif isinstance(term, OtpErlangBinary):
        return term.binary()
    elif isinstance(term, OtpErlangFunction):
        return term.binary()
    elif isinstance(term, OtpErlangReference):
        return term.binary()
    elif isinstance(term, OtpErlangPort):
        return term.binary()
    elif isinstance(term, OtpErlangPid):
        return term.binary()
    else:
        raise OutputException('unknown python type')

# (term_to_binary Erlang term composite type functions)

def _string_to_binary(term):
    length = len(term)
    if length == 0:
        return b_chr(_TAG_NIL_EXT)
    elif length <= 65535:
        return b_chr(_TAG_STRING_EXT) + struct.pack(b'>H', length) + term
    elif length <= 4294967295:
        return (
            b_chr(_TAG_LIST_EXT) + struct.pack(b'>I', length) +
            b''.join([b_chr(_TAG_SMALL_INTEGER_EXT) + b_chr(b_ord(c))
                      for c in term]) +
            b_chr(_TAG_NIL_EXT)
        )
    else:
        raise OutputException('uint32 overflow')

def _tuple_to_binary(term):
    length = len(term)
    if length <= 255:
        return (
            b_chr(_TAG_SMALL_TUPLE_EXT) + b_chr(length) +
            b''.join([_term_to_binary(element) for element in term])
        )
    elif length <= 4294967295:
        return (
            b_chr(_TAG_LARGE_TUPLE_EXT) + struct.pack(b'>I', length) +
            b''.join([_term_to_binary(element) for element in term])
        )
    else:
        raise OutputException('uint32 overflow')

def _dict_to_binary(term):
    length = len(term)
    if length <= 4294967295:
        return (
            b_chr(_TAG_MAP_EXT) + struct.pack(b'>I', length) +
            b''.join([_term_to_binary(key) + _term_to_binary(value)
                      for key, value in term.items()])
        )
    else:
        raise OutputException('uint32 overflow')

# (term_to_binary Erlang term primitive type functions)

def _integer_to_binary(term):
    if 0 <= term <= 255:
        return b_chr(_TAG_SMALL_INTEGER_EXT) + b_chr(term)
    return b_chr(_TAG_INTEGER_EXT) + struct.pack(b'>i', term)

def _long_to_binary(term):
    if -2147483648 <= term <= 2147483647:
        return _integer_to_binary(term)
    return _bignum_to_binary(term)

def _bignum_to_binary(term):
    bignum = abs(term)
    if term < 0:
        sign = b_chr(1)
    else:
        sign = b_chr(0)
    value = []
    while bignum > 0:
        value.append(b_chr(bignum & 255))
        bignum >>= 8
    length = len(value)
    if length <= 255:
        return (
            b_chr(_TAG_SMALL_BIG_EXT) +
            b_chr(length) + sign + b''.join(value)
        )
    elif length <= 4294967295:
        return (
            b_chr(_TAG_LARGE_BIG_EXT) +
            struct.pack(b'>I', length) + sign + b''.join(value)
        )
    else:
        raise OutputException('uint32 overflow')

def _float_to_binary(term):
    return b_chr(_TAG_NEW_FLOAT_EXT) + struct.pack(b'>d', term)

# Exception classes listed alphabetically

class InputException(ValueError):
    """
    InputError describes problems with function input parameters
    """
    def __init__(self, s):
        ValueError.__init__(self)
        self.__s = str(s)
    def __str__(self):
        return self.__s

class OutputException(TypeError):
    """
    OutputError describes problems with creating function output data
    """
    def __init__(self, s):
        TypeError.__init__(self)
        self.__s = str(s)
    def __str__(self):
        return self.__s

class ParseException(SyntaxError):
    """
    ParseError provides specific parsing failure information
    """
    def __init__(self, s):
        SyntaxError.__init__(self)
        self.__s = str(s)
    def __str__(self):
        return self.__s

def consult(string_in):
    """
    provide file:consult/1 functionality with python types
    """
    # pylint: disable=eval-used
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    # manually parse textual erlang data to avoid external dependencies
    list_out = []
    tuple_binary = False   # binaries become tuples of integers
    quoted_string = False  # strings become python string
    atom_string = False    # atoms become python string
    number = False
    whitespace = frozenset(('\n', '\t', ' '))
    i = 0
    while i < len(string_in):
        character = string_in[i]
        if character == ',':
            if atom_string:
                list_out.append('"')
                atom_string = False
            list_out.append(',')
            number = string_in[i + 1].isdigit()
        elif character == '{':
            list_out.append('(')
            number = string_in[i + 1].isdigit()
        elif character == '}':
            if atom_string:
                list_out.append('"')
                atom_string = False
            list_out.append(')')
            number = False
        elif character == '[':
            list_out.append('[')
            number = string_in[i + 1].isdigit()
        elif character == ']':
            if atom_string:
                list_out.append('"')
                atom_string = False
            list_out.append(']')
            number = False
        elif character == '<' and string_in[i + 1] == '<':
            list_out.append('(')
            tuple_binary = True
            i += 1
        elif character == '>' and string_in[i + 1] == '>':
            list_out.append(')')
            tuple_binary = False
            i += 1
        elif not quoted_string and not atom_string and character in whitespace:
            number = string_in[i + 1].isdigit()
        elif tuple_binary or number:
            list_out.append(character)
        elif character == '"':
            if quoted_string:
                quoted_string = False
            else:
                quoted_string = True
            list_out.append('"')
        elif character == "'":
            if atom_string:
                atom_string = False
            else:
                atom_string = True
            list_out.append('"')
        elif not quoted_string and not atom_string:
            atom_string = True
            list_out.append('"')
            list_out.append(character)
        else:
            list_out.append(character)
        i += 1
    return eval(''.join(list_out))
