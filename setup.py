import setuptools
setuptools.setup(
    name="MovieHeavens",
    version="1.0.1",
    py_modules=['movies','movieSource.MovieHeaven','movieSource.fake_user_agent'],
    entry_points={'gui_scripts': ['MovieHeavens = movies:_main']},
    install_requires=['PyQt5','requests','fake-useragent'],
    include_package_data=True
)
