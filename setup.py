try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(
		name = "py-applescript",
		version = "1.0.1",
		description = "An easy-to-use Python wrapper for NSAppleScript, allowing Python scripts to communicate with AppleScripts and AppleScriptable applications.",
		platforms = ['Mac OS X'],
		license = 'Public Domain',
		packages = ['applescript'],
		requires = ['pyobjc'],
		classifiers = [
			'License :: Public Domain',
			'Development Status :: 5 - Production/Stable',
			'Operating System :: MacOS :: MacOS X',
			'Programming Language :: Python :: 2.7',
			'Programming Language :: Python :: 3',
		],

)
