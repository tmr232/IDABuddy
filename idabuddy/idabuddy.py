import os
import random
import yaml
from sark.qt import QtCore, QtWidgets, QtGui, connect_method_to_signal

import idaapi

idaapi.require('interaction')
from interaction import ask_ok

CONFIG = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'rb'))
AUTO_POPUP_TIMEOUT = CONFIG['popup']['timeout']
POPUP_PROBABILITY = CONFIG['popup']['probability']
TALKBUBBLE_STYLESHEET = CONFIG['stylesheet']
ANIMATION_DURATION = CONFIG['animation']['duration']
IDABUDDY_AVATAR_PATH = os.path.join(os.path.dirname(__file__), CONFIG['image'])


# TODO: use a layout instead of those weird positioning tricks.


class TalkBubble(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super(TalkBubble, self).__init__(*args, **kwargs)

        self.setStyleSheet(TALKBUBBLE_STYLESHEET)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setWordWrap(True)


class Slide(QtWidgets.QWidget):
    def initialize(self):
        self.adjustSize()
        self.setFixedSize(self.size())
        self.animations = []
        self.animation_group = QtCore.QParallelAnimationGroup()
        easing_curve = QtCore.QEasingCurve(QtCore.QEasingCurve.InCubic)
        for child in self.children():
            animation = QtCore.QPropertyAnimation(child, 'pos')
            animation.setDuration(ANIMATION_DURATION)
            animation.setStartValue(child.pos())
            animation.setEndValue(QtCore.QPoint(child.x(), self.height()))
            animation.setEasingCurve(easing_curve)
            self.animations.append(animation)
            self.animation_group.addAnimation(animation)
        self.animation_group.start()
        self.animation_group.setCurrentTime(self.animation_group.totalDuration())

    def set_on_animation_end(self, callback):
        connect_method_to_signal(self.animation_group, 'finished()', callback)

    def slide_out(self):
        animation_group = self.animation_group
        animation_group.setDirection(QtCore.QAbstractAnimation.Forward)

        if (animation_group.state() == QtCore.QAbstractAnimation.Stopped and
                    animation_group.currentTime() == animation_group.totalDuration()):
            return

        animation_group.start()

    def slide_in(self):
        animation_group = self.animation_group
        animation_group.setDirection(QtCore.QAbstractAnimation.Backward)

        if (animation_group.state() == QtCore.QAbstractAnimation.Stopped and
                    animation_group.currentTime() == 0):
            return

        animation_group.start()

    @property
    def is_in(self):
        return (self.animation_group.state() == QtCore.QAbstractAnimation.Stopped and
                self.animation_group.currentTime() == 0)

    @property
    def is_out(self):
        return (self.animation_group.state() == QtCore.QAbstractAnimation.Stopped and
                self.animation_group.currentTime() == 0)


class Popup(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(Popup, self).__init__(*args, **kwargs)

        pm = QtGui.QPixmap(IDABUDDY_AVATAR_PATH)
        transform = QtGui.QTransform()
        transform.scale(0.5, 0.5)
        self.pm = pm.transformed(transform)

        self.slide = Slide(self)

        self.image_label = QtWidgets.QLabel(self.slide)
        self.image_label.setPixmap(self.pm)

        self.image_label.setFixedSize(self.pm.size())
        self.image_label.setAlignment(QtCore.Qt.AlignTop)
        self.slide.initialize()
        self.talk_bubble = TalkBubble(self)

        self.talk_bubble.move(0, 0)
        self.talk_bubble.hide()
        self.slide.move(size_to_point(self.talk_bubble.size()))

        self.setFixedSize(self.talk_bubble.size() + self.slide.size())

        connect_method_to_signal(self.talk_bubble, 'linkActivated(QString)', self.linkActivatedHandler)
        self._handlers = {}
        self._default_handler = None

    def _unhandled_link(self, link):
        self.message('Your code did not handle <code>{link}</code> and now I\'m confused.'.format(link=link))

    def linkActivatedHandler(self, link):
        handler = self._handlers.get(link, self._default_handler)
        if handler is None:
            self._unhandled_link(link)
        else:
            handler(link, self)

    def set_handlers(self, default_handler=None, **handlers):
        self._handlers = handlers
        self._default_handler = default_handler

    def setText(self, text):
        if not text:
            self.talk_bubble.hide()
        else:
            self.talk_bubble.setText(text)
            self.talk_bubble.adjustSize()
            self.talk_bubble.show()
            self.talk_bubble.move(0, 0)
            self.slide.move(size_to_point(self.talk_bubble.size()))

        self.setFixedSize(self.talk_bubble.size() + self.slide.size())

    def exit(self):
        self.setText(None)
        self.slide.slide_out()

    def enter(self):
        self.setText(None)
        self.slide.slide_in()

    def say(self, text):
        # TODO: There might still be an issue if after `enter` is called, the animation finishes before setting
        # TODO: the event.
        self.set_handlers()
        if not self.slide.is_in:
            self.enter()
            self.slide.set_on_animation_end(lambda: self.setText(text) if self.slide.is_in else None)
        else:
            self.setText(text)

    def interact(self, text, default_handler=None, **handlers):
        self.say(text)
        self.set_handlers(default_handler=default_handler, **handlers)

    def message(self, text):
        self.interact(ask_ok(text), default_handler=lambda *ignored: self.exit())


class AutoPopup(Popup):
    def __init__(self, *args, **kwargs):
        super(AutoPopup, self).__init__(*args, **kwargs)

        self._auto_timer = QtCore.QTimer()
        connect_method_to_signal(self._auto_timer, 'timeout()', self._on_timer)

        self._callbacks = []
        self._count = 0

    def automate(self, *callbacks):
        self._callbacks = callbacks

    def _on_timer(self):
        if random.random() < POPUP_PROBABILITY:
            self._auto_timer.stop()
            random.choice(self._callbacks)(self)

    def start(self):
        self._auto_timer.start(AUTO_POPUP_TIMEOUT)

    def stop(self):
        self._auto_timer.stop()

    def exit(self):
        super(AutoPopup, self).exit()
        self._auto_timer.start()


def size_to_point(size):
    return QtCore.QPoint(size.width(), size.height())


def get_text_size(text, font):
    font_metrics = QtWidgets.QFontMetrics(font)
    text_size = font_metrics.size(0, text)  # Flags set to `0` to allow linebreaks.
    return text_size

# TODO: sync all IDABuddies to avoid having multiple buddies on at the same time.
