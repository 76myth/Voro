from setuptools import setup, find_packages

setup(
    name = "Voro",
    version = "0.1",
    packages = find_packages(),
    include_package_data = True,
    install_requires = ['beautifulsoup'],
    zip_safe = False,
    entry_points = {
        'console_scripts': [
	'voro-example = voro.scripts.example:main'],
	}
)
