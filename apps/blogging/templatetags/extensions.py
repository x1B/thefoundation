import re

from django import template
from django.utils.translation import gettext_lazy as _


register = template.Library()
r_expr = re.compile(r'(.*?)\s+as\s+(\w+)', re.DOTALL)


class ExprNode(template.Node):
    """{% expr PYTHON_EXPR as VAR_NAME %}"""
    """See http://www.djangosnippets.org/snippets/9/"""
    def __init__(self, expr_string, var_name):
        self.expr_string = expr_string
        self.var_name = var_name

    def render(self, context):
        try:
            clist = list(context)
            clist.reverse()
            d = {}
            d['_'] = _
            for c in clist:
                d.update(c)
            if self.var_name:
                context[self.var_name] = eval(self.expr_string, d)
                return ''
            else:
                return str(eval(self.expr_string, d))
        except:
            raise


@register.tag(name='expr')
def do_expr(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents[0]
    m = r_expr.search(arg)
    if m:
        expr_string, var_name = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError, "%r tag at least requires one argument" % tag_name
        expr_string, var_name = arg, None
    return ExprNode(expr_string, var_name)
