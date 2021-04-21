from setuptools import setup

setup(
    name='python-patho',
    version='0.1.1',    
    description='Python library for pathology image analysis',
    url='https://github.com/superizer/pypath',
    author='Attasuntorn Traisuwan',
    author_email='superizer.tone@gmail.com',
    license='AGPL-3.0 License',
    packages=['pypath'],
    install_requires=['numpy', 'opencv-python'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.6',
    ],
)