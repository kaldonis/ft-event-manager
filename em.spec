# -*- mode: python -*-
a = Analysis(['src\\main.py'],
             pathex=['src\\lib', 'src'],
             hiddenimports=['app.handlers.event', 'app.forms.event', 'app.handlers.admin', 'app.handlers.base', 'app.handlers.bot', 'app.handlers.bracket', 'app.handlers.static', 'app.forms.bot', 'app.forms.bracket', 'app.domain.bot_status', 'app.domain.constants', 'app.domain.format', 'app.models.bot', 'app.models.bracket', 'app.models.category', 'app.models.database', 'app.models.event', 'app.models.match', 'app.models.weightclass', 'webapp2_static',
							'wtforms', 'wtforms.validators', 'wtforms.ValidationError', 'wtforms.SubmitField', 'wtforms.DateField', 'wtforms.StringField', 'wtforms.Form', 'wtforms.compat', 'wtforms.compat.string_types', 'wtforms.compat.text_type', 'wtforms.widgets', 'wtforms.widgets.core', 'wtforms.fields', 'wtforms.csrf', 'wtforms.ext', 'wtforms.locale', 'wtforms.fields.core', 'decimal', 'numbers', 'math', 'copy', 'wtforms.i18n', 'wtforms.form', 'wtforms.meta', 'wtforms.utils', 'wtforms.fields.simple'],
             hookspath=None,
             runtime_hooks=None)
template_tree = Tree('src\\templates', prefix='templates')
static_tree = Tree('src\\static', prefix='static')
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
		  template_tree,
		  static_tree,
          name='em.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
