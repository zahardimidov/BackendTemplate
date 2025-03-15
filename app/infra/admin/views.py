from sqladmin import ModelView

from app.infra.database.models import User


class AdminView(ModelView):
    ...


class UserAdmin(AdminView, model=User):
    form_include_pk = True

    column_list = [User.id, User.username, User.first_name, User.phone]
    form_columns = [User.id, User.username, User.first_name, User.phone]
