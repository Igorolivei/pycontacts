from setuptools import setup

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pymongo'
]

setup(name='contact_book',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = contact_book:main
      """,
)