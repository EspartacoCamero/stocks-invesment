from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    version='0.1.0',
    description='This project will tell you where to invest your money according to your prefered stocks',
    author='Espartaco Camero',
    license='',
    entry_points={
        'console_scripts': [
            'stocks_inv_make_dataset = data.make_dataset:main'
        ],
    }
)
