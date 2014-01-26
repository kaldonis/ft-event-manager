import json
from app.handlers.base import BaseHandler

# imports needed for eval
from app.models.weightclass import Weightclass
from app.models.category import BotCategory

ALLOWED_TABLES = ['Weightclass', 'BotCategory']
ACTION_EDIT = 'edit'
ACTION_DELETE = 'delete'

class AdminHandler(BaseHandler):
    """
    renders the admin page
    """
    def get(self):
        context = {
            'tables': ALLOWED_TABLES
        }
        self.render_response('admin.html', **context)


class EditTableHandler(BaseHandler):
    """
    handler for editing a code table (weightclass, categories, etc?)
    """

    def get(self, table):
        """ get """
        if table not in ALLOWED_TABLES:
            self.redirect_to('home')

        context = {
            'table_name': table
        }

        table = eval(table)
        rows = table.get_all()

        context.update({
            'table_data': json.dumps([row.to_dict() for row in rows if row ]),
            'editable_fields': table.EDITABLE_FIELDS,
            'row_template': json.dumps(dict(zip(table.EDITABLE_FIELDS, ['' for _ in table.EDITABLE_FIELDS])))
        })
        self.render_response('edit-table.html', **context)

    def post(self, table, action):
        """ post """
        if table not in ALLOWED_TABLES or action not in [ACTION_DELETE, ACTION_EDIT]:
            self.redirect_to('home')

        table = eval(table)
        data = dict(self.request.params.items())

        if action == ACTION_EDIT:
            # existing row, update
            if data.get('id'):
                row = table.get_by_id(data['id'])
                for field, value in data.iteritems():
                    if field in table.EDITABLE_FIELDS:
                        setattr(row, field, value)
            else:  # new row, add
                row = table(**data)
            error = row.put()
        else:
            row = table.get_by_id(data['id'])
            error = row.delete()

        if not error:
            response = {
                'successful': True,
                'id': row.id
            }
        else:
            response = {
                'successful': False,
                'message': error
            }

        context = {
            'data': json.dumps(response)
        }

        self.render_response('json.json', **context)