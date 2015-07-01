from setuptools import setup
 
setup(name='chat',
      version='0.0.1',
      description='Basic Chat Service',
      author='Matt Hall',
      author_email='matt@matthall.tv',
      url='http://matthall.tv',
      packages=['chat'],
      package_data={'twisted.plugins': ['twisted/plugins/chat.py']},
      zip_safe=False
)
