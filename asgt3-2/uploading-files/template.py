import os
import cgi
import string
import cStringIO


def escape(s):
    return cgi.escape(s, quote=True)


def variable():
    return cStringIO.StringIO()


def render(filename, mapping=None, escaped=True):
    with open(os.path.join('templates', filename)) as f:
        template = string.Template(f.read())

    if mapping:
        mapping = {
            k: v.getvalue() if hasattr(v, 'getvalue') else str(v)
                for k, v in mapping.iteritems()
        }

        if escaped:
            mapping = {k: escape(v) for k, v in mapping.iteritems()}
    else:
        mapping = {}

    return template.substitute(mapping)
