from flask.cli import AppGroup
from .auth import auth
# from .providers import get_ldap_user_info


# class CreateUserCommand(BaseCreateUserCommand):

#     option_list = BaseCreateUserCommand.option_list + (
#         Option('-i', '--id', dest='id', default=None),
#         Option('-l', '--ldap', dest='is_ldap', action='store_true'),
#         Option('-n', '--name', dest='name'),
#     )

#     def run(self, **kwargs):
#         user_id = kwargs['id']
#         is_ldap_user = kwargs['is_ldap']

#         if is_ldap_user:
#             ldap_user_info = get_ldap_user_info(user_id)
#             if ldap_user_info is None:
#                 print("No such LDAP user: %r" % user_id)
#                 return
#             kwargs['password'] = 'password is ignored'
#             kwargs['email'] = ldap_user_info['email']

#         super(CreateUserCommand, self).run(**kwargs)

#         if is_ldap_user:
#             auth.models.RegisteredUser.query.get(user_id).password = None
#             auth.models.db.session.commit()


# user_manager = Manager()
# user_manager.add_command('create', CreateUserCommand())
# user_manager.add_command('deactivate', DeactivateUserCommand())
# user_manager.add_command('activate', ActivateUserCommand())

user_manager = AppGroup("user")


@user_manager.command
def ls():
    for user in auth.models.RegisteredUser.query:
        print(f"{user.id} <{user.email}>")


@user_manager.command
def activate(user_id):
    from art17.auth.common import set_user_active

    user = auth.models.RegisteredUser.query.get(user_id)
    set_user_active(user, True)
    print(f"user {user.id} has been activated")


@user_manager.command
def deactivate(user_id):
    from art17.auth.common import set_user_active

    user = auth.models.RegisteredUser.query.get(user_id)
    set_user_active(user, False)
    print(f"user {user.id} has been deactivated")


@user_manager.command
def remove(user_id):
    user = auth.models.RegisteredUser.query.get(user_id)
    auth.models.db.session.delete(user)
    auth.models.db.session.commit()


@user_manager.command
def info(user_id):
    user = auth.models.RegisteredUser.query.get(user_id)
    print(user.id)
    print(f"name: {user.name}")
    print(f"active: {user.active}")
    print(f"ldap: {user.is_ldap}")
    print(f"roles: {[r.name for r in user.roles]}")


@user_manager.command
def reset_password(user_id):
    from flask.ext.security.utils import encrypt_password

    user = auth.models.RegisteredUser.query.get(user_id)
    if user.is_ldap:
        print("Can't change password for EIONET users")
        return
    plaintext_password = input("new password: ").decode("utf-8")
    user.password = encrypt_password(plaintext_password)
    auth.models.db.session.commit()
    print(f"password for {user_id} has been changed")


# role_manager = Manager()
# role_manager.add_command('create', CreateRoleCommand())
# role_manager.add_command('add', AddRoleCommand())
# role_manager.add_command('remove', RemoveRoleCommand())

role_manager = AppGroup("role")


@role_manager.command
def ls():
    for role in auth.models.Role.query:
        print(f"{role.name}: {role.description}")


@role_manager.command
def members(role):
    role_ob = auth.models.Role.query.filter_by(name=role).first()
    if role_ob is None:
        print("No such role %r" % role)
        return
    for user in role_ob.users:
        print(f"{user.id} <{user.email}>")
