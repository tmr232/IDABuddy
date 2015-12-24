import os


class Link(object):
    DEFAULTS = dict(color='inherit', text_decoration='None')

    def __init__(self, text, href=None, **style):
        self.text = text
        if href is None:
            self.href = text
        else:
            self.href = href
        self.style = self.DEFAULTS.copy()
        self.style.update(style)

    def __str__(self):
        return '<a href="{href}" style="{style}">{text}</a>'.format(
            href=self.href,
            text=self.text,
            style=';'.join('{}:{}'.format(key.replace('_', '-'), value) for key, value in self.style.iteritems())
        )


class Span(object):
    DEFAULTS = dict()

    def __init__(self, text, href=None, **style):
        self.text = text
        self.style = self.DEFAULTS.copy()
        self.style.update(style)

    def __str__(self):
        return '<span style="{style}">{text}</span>'.format(
            text=self.text,
            style=';'.join('{}:{}'.format(key.replace('_', '-'), value) for key, value in self.style.iteritems())
        )


def yes_no():
    yes = Link('Yes', href='yes', color='green', text_decoration='underscore')
    no = Link('No', href='no', color='red', text_decoration='underscore')
    return '{yes}    {no}'.format(yes=yes, no=no)


def nxt():
    return Link('Next', href='next', color='blue', text_decoration='underscore')


def ok():
    return Link('Ok', href='ok', color='blue', text_decoration='underscore')


def ask_next(query):
    return '{query}{br}{next}'.format(**use_defaults(query=query))


def ask_ok(query):
    return '{query}{br}{ok}'.format(**use_defaults(query=query))


FORM_DEFAULTS = dict(yesno=yes_no(), br='<br/>', ok=ok(), next=nxt())


def use_defaults(**kwargs):
    defaults = FORM_DEFAULTS.copy()
    defaults.update(kwargs)
    return defaults


def ask_yes_no(query):
    return '{query}{br}{yesno}'.format(**use_defaults(query=query))


class ImageGetter(object):
    def __getitem__(self, key):
        return '<img src="{path}"/>'.format(path=os.path.join(os.path.dirname(__file__), key))


def embed_images(phrase):
    return phrase.format(image=ImageGetter())