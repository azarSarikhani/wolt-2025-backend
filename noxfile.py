import nox


@nox.session
def typecheck(session):
    session.install("mypy", "pylint", "requests")
    session.run('mypy', 'lib/src/')


@nox.session
def tests(session):
    session.install('pytest')
    session.run("python", "-m", "pip", "install", "-e", "lib")
    session.run('pytest', '-v')


@nox.session
def lint(session):
    session.install('flake8')
    session.run('flake8')
