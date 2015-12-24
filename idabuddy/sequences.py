import os
import random

import idaapi
import sark
import yaml

idaapi.require('interaction')

from interaction import ask_next, ask_ok, Link, use_defaults, Span, embed_images

SAYINGS = yaml.load(open(os.path.join(os.path.dirname(__file__), 'sayings.yml'), 'rb'))
BASIC_SAYINGS = SAYINGS['basic']
ADDRESS_SAYINGS = SAYINGS['address']


def go_cancel():
    go = Link('Go', href='go', color='green', text_decoration='underscore')
    cancel = Link('Cancel', href='cancel', color='red', text_decoration='underscore')
    return '{go}    {cancel}'.format(cancel=cancel, go=go)


def ask_go_cancel(query):
    return '{query}{br}{gocancel}'.format(**use_defaults(query=query, gocancel=go_cancel()))


def say_multiple(buddy, *text):
    last_text = text[-1]
    text = iter(text[:-1])

    def _messenger(*args, **kwargs):
        try:
            buddy.interact(ask_next(text.next()), next=_messenger)
        except StopIteration:
            buddy.interact(ask_ok(last_text), ok=lambda *_: buddy.exit())

    _messenger()


def format_saying(saying, use_images=False):
    for phrase in saying:
        # Replace line-breaks with `<br/>` for the rich text viewer.
        yield format_phrase(phrase, use_images)


def format_phrase(phrase, use_images=False):
    phrase = '<br/>'.join(phrase.splitlines())
    if use_images:
        phrase = embed_images(phrase)
    return (phrase)


def say_random_saying(buddy):
    say_multiple(buddy, *format_saying(random.choice(BASIC_SAYINGS), use_images=True))


def say_address(buddy):
    address = get_random_address()
    address_text = Span('0x{address:X}'.format(address=address), color='black', text_decoration='underline')
    buddy.interact(
        ask_go_cancel(random_address_saying().format(address_text)),
        go=lambda *_: (idaapi.jumpto(address), buddy.exit()),
        cancel=lambda *_: buddy.exit())


def random_address_saying():
    return format_phrase(random.choice(ADDRESS_SAYINGS))


def get_random_address():
    segment = random.choice(list(sark.segments()))
    address = random.randint(segment.startEA, segment.endEA)
    return address
