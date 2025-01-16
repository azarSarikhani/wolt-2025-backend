import nox


@nox.session
def tests(session):
    session.install('pytest')
    session.run("python", "-m", "pip", "install", "-e", "lib")
    session.run('pytest', '-v')


#@nox.session
#def lint(session):
#    session.install('flake8')
#    session.run('flake8')