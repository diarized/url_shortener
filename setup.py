from distutils.core import setup

setup(
    name='URLshortener',
    version='0.1',
    author='Artur Kaminski',
    author_email='my.home.my.castle@gmail.com',
    scripts=['gevent_tornado.py', 'pure_tornado.py'],
    url='https://github.com/diarized/url_shortener',
    license='LICENSE.txt',
    description='URL shortener based on non blocking web server',
    long_description=open('README.md').read(),
    install_requires=[
        "tornado >= 2.3",
        "gevent >= 0.13.6",
    ],
)
