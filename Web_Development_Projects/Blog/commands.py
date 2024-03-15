import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash


@click.command("create-admin")
@click.argument("email")
@click.argument("password")
@click.argument("name")
@with_appcontext
def create_admin(email, password, name):
    from main import db, User  # Import locally to avoid circular import

    hashed_password = generate_password_hash(
        password, method='pbkdf2:sha256', salt_length=8
    )
    admin_user = User(email=email, name=name, password=hashed_password, is_admin=True)
    db.session.add(admin_user)
    db.session.commit()
    click.echo(f"Admin {name} created successfully.")
