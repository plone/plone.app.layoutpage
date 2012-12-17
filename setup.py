from setuptools import setup, find_packages

version = '1.1'
tests_require = [
    'plone.testing',
    'plone.app.testing',
    'plone.behavior',
]

setup(
    name='plone.app.layoutpage',
    version=version,
    description="A basic page content type for Plone using Deco layout",
    long_description=open("README.rst").read(),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='David Glick',
    author_email='dglick@gmail.com',
    url='http://github.com/plone/plone.app.layoutpage',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.interface',
        'zope.component',
        'zope.lifecycleevent',
        'z3c.form',
        'Zope2',
        'plone.dexterity',
        'plone.app.blocks',
        'plone.app.dexterity',
    ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
