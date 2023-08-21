import click


@click.group()
def cli():
    """
        Application from GEO calculation
    """


@cli.group()
def db():
    """
        Database context
    """


@cli.group()
def tasks():
    """
        Tasks context
    """


@cli.command()
def runserver():
    """
        Start http server
    """
    from application import app

    app.run()


@db.command()
def create():
    """
        Create new Database or flush exists
    """
    from application import app, db

    app.app_context().push()
    db.drop_all()
    db.create_all()
    db.session.commit()


@tasks.command()
def show():
    """
        Show tasks summary
    """
    from application import app
    from application.services.tasks import TasksService

    app.app_context().push()

    summary = TasksService.get_summary()
    print(f"Tasks count: {summary['total']}")
    if summary['total']:
        print(80 * '=')
        for status, count in summary['distribution']:
            print(f"status={status.value}: {count}")
        print(80 * '=')
        for task in summary['tasks']:
            print(str(task))


@tasks.command()
def clean():
    """
        Clean up all tasks
    """
    from application import app
    from application.services.tasks import TasksService

    app.app_context().push()

    TasksService.cleanup()


if __name__ == '__main__':
    cli()
