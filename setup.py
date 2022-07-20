from setuptools import setup

# Requirements used for submodules
# plot = ['plotly>=4.0']
# hyperopt = [
#     'scipy',
#     'scikit-learn',
#     'scikit-optimize>=0.7.0',
#     'filelock',
#     'joblib',
#     'progressbar2',
# ]

# develop = [
#     'coveralls',
#     'flake8',
#     'flake8-tidy-imports',
#     'mypy',
#     'pytest',
#     'pytest-asyncio',
#     'pytest-cov',
#     'pytest-mock',
#     'pytest-random-order',
# ]

# jupyter = [
#     'jupyter',
#     'nbstripout',
#     'ipykernel',
#     'nbconvert',
# ]

# all_extra = plot + develop + jupyter + hyperopt

setup(
    # name='conversation-filter-kr',
    # version='1.0',
    # description='Filter conversations made in Korean language',
    # license="MIT",
    # # long_description=long_description,
    # # author='Man Foo',
    # # author_email='foomail@foo.example',
    # # url="http://www.foopackage.example/",
    # packages=['twoturn_filter'],  #same as name
    install_requires=[
                'pandas',
                'transformers',
                'torch',
            ],
    # scripts=[
    #             'scripts/cool',
    #             'scripts/skype',
    #         ]
    # tests_require=[
    #     'pytest',
    #     'pytest-asyncio',
    #     'pytest-cov',
    #     'pytest-mock',
    # ],
    # extras_require={
    #     'dev': all_extra,
    #     'plot': plot,
    #     'jupyter': jupyter,
    #     'hyperopt': hyperopt,
    #     'all': all_extra,
    # },
)