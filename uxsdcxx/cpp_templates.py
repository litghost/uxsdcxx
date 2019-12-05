from string import Template

# See https://www.obj-sys.com/docs/xbv23/CCppUsersGuide/ch04.html.
atomic_builtins = {
	"string": "const char *",
	"boolean": "bool",
	"float": "float",
	"decimal": "int",
	"integer": "int",
	"nonPositiveInteger": "int",
	"negativeInteger": "int",
	"long": "long",
	"int": "int",
	"short": "short",
	"byte": "char",
	"nonNegativeInteger": "unsigned int",
	"unsignedLong": "unsigned long",
	"unsignedInt": "unsigned int",
	"unsignedShort": "unsigned short",
	"unsignedByte": "unsigned byte",
	"positiveInteger": "unsigned int",
	"double": "double",
	"IDREF": "const char *",
	"ID": "const char *",
	"NCName": "const char *",
}

atomic_builtin_load_formats = {
	"string": "char_pool.add(%s)",
	"boolean": "std::strtol(%s, NULL, 10)",
	"float": "std::strtof(%s, NULL)",
	"decimal": "std::strtol(%s, NULL, 10)",
	"integer": "std::strtol(%s, NULL, 10)",
	"nonPositiveInteger": "std::strtol(%s, NULL, 10)",
	"negativeInteger": "std::strtol(%s, NULL, 10)",
	"long": "std::strtoll(%s, NULL, 10)",
	"int": "std::strtol(%s, NULL, 10)",
	"short": "std::strtol(%s, NULL, 10)",
	"byte": "std::strtol(%s, NULL, 10)",
	"nonNegativeInteger": "std::strtoul(%s, NULL, 10)",
	"unsignedLong": "std::strtoull(%s, NULL, 10)",
	"unsignedInt": "std::strtoul(%s, NULL, 10)",
	"unsignedShort": "std::strtoul(%s, NULL, 10)",
	"unsignedByte": "std::strtoul(%s, NULL, 10)",
	"positiveInteger": "std::strtoul(%s, NULL, 10)",
	"double": "std::strtod(%s, NULL)",
	"IDREF": "char_pool.add(%s)",
	"ID": "char_pool.add(%s)",
	"NCName": "char_pool.add(%s)",
}

cpp_keywords = ["alignas", "alignof", "and", "and_eq", "asm", "atomic_cancel", "atomic_commit", "atomic_noexcept",
			"auto", "bitand", "bitor", "bool", "break", "case", "catch", "char", "char8_t", "char16_t", "char32_t", "class",
			"compl", "concept", "const", "consteval", "constexpr", "const_cast", "continue", "co_await", "co_return",
			"co_yield", "decltype", "default", "delete", "do", "double", "dynamic_cast", "else", "enum", "explicit",
			"export", "extern", "false", "float", "for", "friend", "goto", "if", "inline", "int", "long", "mutable",
			"namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator", "or", "or_eq", "private",
			"protected", "public", "reflexpr", "register", "reinterpret_cast", "requires", "return", "short", "signed",
			"sizeof", "static", "static_assert", "static_cast", "struct", "switch", "synchronized", "template", "this",
			"thread_local", "throw", "true", "try", "typedef", "typeid", "typename", "union", "unsigned", "using",
			"virtual", "void", "volatile", "wchar_t", "while", "xor", "xor_eq"]

header_comment = Template("""#pragma once
/*
 * This file is generated by uxsdcxx $version.
 * https://github.com/duck2/uxsdcxx
 * Modify only if your build process doesn't involve regenerating this file.
 *
 * Cmdline: $cmdline
 * Input file: $input_file
 * md5sum of input file: $md5
 */
""")

impl_comment = Template("""/*
 * This file is generated by uxsdcxx $version.
 * https://github.com/duck2/uxsdcxx
 * Modify only if your build process doesn't involve regenerating this file.
 *
 * Cmdline: $cmdline
 * Input file: $input_file
 * md5sum of input file: $md5
 */
""")

includes = """
#include <bitset>
#include <cassert>
#include <cstring>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

#include <error.h>
#include <stddef.h>
#include <stdint.h>
#include "pugixml.hpp"
"""

dfa_error_decl = """
/**
 * Internal error function for xs:choice and xs:sequence validators.
 */
inline void dfa_error(const char *wrong, int *states, const char **lookup, int len);
"""

all_error_decl = """
/**
 * Internal error function for xs:all validators.
 */
template<std::size_t N>
inline void all_error(std::bitset<N> gstate, const char **lookup);
"""

attr_error_decl = """
/**
 * Internal error function for attribute validators.
 */
template<std::size_t N>
inline void attr_error(std::bitset<N> astate, const char **lookup);
"""

dfa_error_defn = """
inline void dfa_error(const char *wrong, int *states, const char **lookup, int len){
	std::vector<std::string> expected;
	for(int i=0; i<len; i++){
		if(states[i] != -1) expected.push_back(lookup[i]);
	}

	std::string expected_or = expected[0];
	for(unsigned int i=1; i<expected.size(); i++)
		expected_or += std::string(" or ") + expected[i];

	throw std::runtime_error("Expected " + expected_or + ", found " + std::string(wrong));
}
"""

all_error_defn = """
template<std::size_t N>
inline void all_error(std::bitset<N> gstate, const char **lookup){
	std::vector<std::string> missing;
	for(unsigned int i=0; i<N; i++){
		if(gstate[i] == 0) missing.push_back(lookup[i]);
	}

	std::string missing_and = missing[0];
	for(unsigned int i=1; i<missing.size(); i++)
		missing_and += std::string(", ") + missing[i];

	throw std::runtime_error("Didn't find required elements " + missing_and + ".");
}
"""

attr_error_defn = """
template<std::size_t N>
inline void attr_error(std::bitset<N> astate, const char **lookup){
	std::vector<std::string> missing;
	for(unsigned int i=0; i<N; i++){
		if(astate[i] == 0) missing.push_back(lookup[i]);
	}

	std::string missing_and = missing[0];
	for(unsigned int i=1; i<missing.size(); i++)
		missing_and += std::string(", ") + missing[i];

	throw std::runtime_error("Didn't find required attributes " + missing_and + ".");
}
"""
