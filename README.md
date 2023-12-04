py-applescript -- An easy-to-use Python wrapper for NSAppleScript, allowing Python scripts to communicate with AppleScripts and AppleScriptable applications.


Features
========

- scripts may be compiled from source or loaded from disk

- standard 'run' handler and user-defined handlers can be invoked with or without arguments

- argument and result values are automatically converted between common Python types and their AppleScript equivalents

- compiled scripts are persistent: handlers can be called multiple times and top-level properties retain their state

- avoids any dependency on the legacy appscript library, flawed Scripting Bridge framework, or limited osascript executable


Requirements
============

- Python 2.7.x or Python 3.x
- PyObjC


Installation
============

To install the applescript package, cd to the py-applescript-x.x.x directory and run:

  python setup.py install

or:

  python3 setup.py install


Interface
=========

The applescript package exports four classes - AppleScript, ScriptError, AEType and AEEnum - plus one constant, kMissingValue, and one module, kae.


AppleScript
-----------

Represents a compiled AppleScript. The script object is persistent; its handlers may be called multiple times and its top-level properties will retain current state until the script object's disposal.

Properties:

	source : str -- the script's source code

Methods:

	__init__(self, source=None, path=None)
		source : str | None -- AppleScript source code
		path : str | None -- full path to .scpt/.applescript file
	
		Notes:
			- Either the path or the source argument must be provided.
			- If the script cannot be read/compiled, a ScriptError is raised.

	run(self, *args) -- Run the script, optionally passing arguments to its run handler.
		args : anything -- arguments to pass to script, if any; see also supported type mappings documentation
		Result : anything | None -- the script's return value, if any
	
		Notes:
			- The run handler must be explicitly declared in order to pass arguments.
			- AppleScript will ignore excess arguments. Passing insufficient arguments will result in an error.
			- If execution fails, a ScriptError is raised.

	call(self, name, *args) -- Call the specified user-defined handler.
		name : str -- the handler's name (case-sensitive)
		args : anything -- arguments to pass to script, if any; see documentation for supported types
		Result : anything | None -- the script's return value, if any
		
		Notes:
			- The handler's name must be a user-defined identifier, not an AppleScript keyword; e.g. 'myCount' is acceptable; 'count' is not.
			- AppleScript will ignore excess arguments. Passing insufficient arguments will result in an error.
			- If execution fails, a ScriptError is raised.


ScriptError
----------- 

Indicates an AppleScript compilation/execution error.

Properties:

	message : str -- the error message
	number : int | None -- the error number, if given
	appname : str | None -- the name of the application that reported the error, where relevant
	range : (int, int) -- the start and end points (1-indexed) within the source code where the error occurred


AEType
------

An AE type. Maps to an AppleScript type class, e.g. AEType(b'utxt') <=> 'unicode text'.
	
Hashable and comparable, so may be used as keys in dictionaries that map to AE records.

Properties:

	code : bytes -- four-char code, e.g. b'utxt'
	
Methods:

	__init__(self, code)
		code : bytes -- four-char code, e.g. b'utxt'

AEEnum
------

An AE enumeration. Maps to an AppleScript constant, e.g. AEEnum(b'yes ') <=> 'yes'

Properties and methods are same as for AEType.


kMissingValue
-------------

Convenience constant. Contains AEType(b'msng'), i.e. AppleScript's 'missing value' constant.


kae
---

This module contains common AE constants auto-generated from OS X header files. For example: from applescript import kae; kae.typeUnicodeText.


Usage
=====

import applescript

# 1. Run script:

applescript.AppleScript('say "Hello AppleScript"').run()


# 2. Call run handler and user-defined handlers with/without arguments:

scpt = applescript.AppleScript('''
	on run {arg1, arg2}
		say arg1 & " " & arg2
	end run
	
	on foo()
		return "foobar"
	end foo
	
	on Bar(x, y)
		return x * y
	end bar
''')

print(scpt.run('Python', 'Calling')) #-> None
print(scpt.call('foo')) #-> "foobar"
print(scpt.call('Bar', 3, 5)) #-> 15


# 3. A compiled script's state persists until the AppleScript instance is disposed:

scpt = applescript.AppleScript('''
	property _count : 0
	
	on run
		set _count to _count + 1
	end run
''')

print(scpt.run()) #-> 1
print(scpt.run()) #-> 2
print(scpt.run()) #-> 3


# 4. Errors will be reported:

applescript.AppleScript('this is not a valid script')
# applescript.ScriptError: A identifier can't go after this identifier. (-2740) range=12-19



Supported type mappings
=======================

The following Python <=> AppleScript mappings are supported:

	None <=> [no value; see Limitations]
	bool <=> boolean
	int <=> integer [or 'real' in some cases; see Limitations]
	float <=> real
	str <=> text [a.k.a. string, Unicode text]
	bytes <=> data
	list <=> list
	tuple => list [one-way mapping only]
	dict <=> record [with restrictions on keys; see Limitations]
	str <= alias/POSIX file [one-way mapping only; see Limitations]
	pyapplescript.AEType <=> type class [keyword]
	pyapplescript.AEEnum <=> constant [keyword]
	datetime.datetime <=> date [no timezone support; see Limitations]


Limitations:

- Returned values may be PyObjC versions of standard Python types, e.g. objc.pyobjc_unicode rather than str.

- AppleScript's integer type is limited to representing 32-bit signed integers. Python ints outside that range are packed as 64-bit floats instead.

- File-related AppleScript types (e.g. alias, POSIX file) are unpacked as POSIX path strings as they have no direct Python equivalent. AppleScripts which receive path strings from Python should use the POSIX file specifier to convert these to file objects as necessary, e.g. 'set theFile to POSIX file thePath'.

- AppleScript type and constant names do not have a direct Python equivalent, so are represented as AEType and AEEnum instances containing their four-char codes. There is no automatic mapping between human-readable keywords and their equivalent four-char codes. See kae.py for standard type and enum codes recognized by AppleScript.

- AppleScript's 'missing value' constant is mapped to AEType(b'msng'). A kMissingValue constant is provided for convenience.

- AppleScript's date class and the equivalent AE descriptor (typeLongDateTime) do not support time zones. Times are assumed to be in the current time zone.

- Python's None type is mapped to typeNull, which AppleScript treats as literally 'no value'. To pass a 'missing value' constant, use kMissingValue instead.

- Python dicts are packed as AE records, which are roughly equivalent to C structs or Python's namedtuple type, so should not be used as general-purpose key-value collections. Keys must be Python strings or AEType instances; AppleScript will map these to user-defined identifiers or AppleScript/scripting addition/application-defined keywords respectively.

- Record-like AE descriptors such as object specifiers (AppleScript 'references') will be unpacked as nested dicts containing an AEType(b'pcls') key whose value is an AEType instance specifying the descriptor type, and one or more other key-value pairs, e.g.:

	{AEType(b'pcls'): AEType(b'obj '), AEType(b'want'):..., AEType(b'form'):..., AEType(b'seld'):..., AEType(b'from'): ...}

- Dicts containing an AEType(b'pcls') key with an AEType value will be coerced to a record-like descriptor of that type when packed, e.g. {AEType(b'pcls'): AEType(b'obj '),…} would be packed as typeObjectSpecifier. 

- If the AEType(b'pcls') key's value is not an AEType, it will be packed into a normal AE record as an ordinary key-value pair, e.g. {AEType(b'pcls'): "foo",…} -> {class: "foo",…} (note, however, that NSAppleScript will report a coercion error if it tries to return a similar object). 

- Dicts not containing an AEType(b'pcls') key will be packed as a normal AE record.

- Trying to pack unsupported Python types will result in a TypeError.

- Unsupported AppleScript types are not unpacked; the NSAppleEventDescriptor instance is returned as-is.


Known issues
============

- While the applescript package was developed for Python 3.x, it also works on Python 2.7 thanks to its back-porting of various 3.x features. However, earlier versions of Python are not supported.

- AppleScript return values and error messages can often contain non-ASCII characters, which Python 2.7 and some editors/environments may have trouble consuming/displaying. This is not AppleScript's problem. Deal, or use Python 3.x (recommended).

- NSAppleScript provides only limited functionality. For example, script object cannot be saved back to disk (so any changes to the script's state will be lost when the AppleScript instance is disposed of); styled source code cannot be obtained; return values cannot be formatted for display as AppleScript-style strings; restrictions apply to multi-threaded use. The OSAKit framework does provide such features (and the legacy Carbon OSA API provides even more). However, the OSAKit framework, while public, is undocumented and the OSA's future in general is uncertain given the deprecation of the underlying Carbon Component Manager API upon which it is built, so has not been used here.

- Object specifiers (AppleScript 'references') returned by NSAppleScript are not fully qualified - i.e. they do not contain the address of the application at which they were targeted - so cannot usefully be passed back to AppleScript in a subsequent call as AppleScript would then treat them as targeting the current process, which is almost probably incorrect. (FWIW, AppleScripts may themselves work around this limitation by wrapping a reference value in a script object and returning that, though this is clumsy as the next AppleScript to which the script object is passed must know how to unwrap it again.)

- NSAppleScript may sometimes write a "NSMapInsert(): attempt to insert notAKeyMarker " warning to stderr when returning error information. This is a bug in NSAppleScript, but should not affect operation.


See Also
========

- https://developer.apple.com/library/mac/#documentation/AppleScript/Conceptual/AppleScriptX

- https://developer.apple.com/library/mac/#documentation/Cocoa/Reference/Foundation/Classes/nsappleeventdescriptor_Class

- https://developer.apple.com/library/mac/#documentation/Cocoa/Reference/Foundation/Classes/nsapplescript_Class

- http://pythonhosted.org/pyobjc


Copyright
=========

py-applescript is released into the public domain. No warranty, E&OE; use at own risk, etc.
