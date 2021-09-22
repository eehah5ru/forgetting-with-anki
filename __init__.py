from sys import stderr, stdout
from anki import hooks
from anki.hooks import wrap
from anki import version as anki_version
import aqt
from aqt.webview import AnkiWebView
from aqt import mw
import random
import re
# from bs4 import BeautifulSoup, Tag

#
# anki version checker
#
# from: https://github.com/ijgnd/anki__editor__apply__font_color__background_color__custom_class__custom_style/blob/95763a4578f527f2e46f05ece90bd5296eed1ee7/src/vars.py
def is_old_anki():
    return tuple(int(i) for i in anki_version.split(".")) < (2, 1, 20)

#
# base pathes
#
addon = mw.addonManager.addonFromModule(__name__)
base="../_addons/" + addon

# add the assests folder to the media server
mw.addonManager.setWebExports(__name__, r".+(\.svg|\.png|\.css|\.woff|\woff2|\.jpeg|\.gif|\.tiff|\.bmp|\.jpg|\.js|\.TTF|\.ttf|\.otf)")

# inject css
# https://github.com/ShoroukAziz/Beautify-Anki/blob/master/__init__.py
#
# webview hook:
# see details: https://github.com/ankitects/anki/blob/main/qt/tools/genhooks_gui.py
# def on_webview_will_set_content(web_content,
#                                 context):

#     if not isinstance(context, aqt.reviewer.Reviewer):
#         # not reviewer, do not modify content
#         return

#     # reviewer, perform changes to content
#     context: aqt.reviewer.Reviewer

#     web_content.css.append(base + "/assets/main.css")
#     web_content.js.append(base + "/assets/vendor/jquery-3.6.0.min.js")
#     web_content.js.append(base + "/assets/main.js")
#     # note = mw.reviewer.card.note()

#     # if 'color' in note.keys():
#     #     color = note['color']
#     #     web_content.head += f"<style>.card {{ background-color: {color}; }}</style>"
#     #     stderr.write(web_content.body)
#     # web_content.body += f"<style>.card {{ background-color: cyan; }}</style>"

# what is wrapping
# def wrap(old, new, pos="after"):
#     "Override an existing function."
#     def repl(*args, **kwargs):
#         if pos == "after":
#             old(*args, **kwargs)
#             return new(*args, **kwargs)
#         elif pos == "before":
#             new(*args, **kwargs)
#             return old(*args, **kwargs)
#         else:
#             return new(_old=old, *args, **kwargs)

# target signature: def stdHtml(self, body, css=None, js=None, head=""):
def addForgettingAssets(self, body, css=None, js=None, head="", _old=None):
    if css is None:
        css = []

    if js is None:
        js = []

    css.append(base + "/user_files/assets/main.css")

    js.append(base + "/user_files/assets/vendor/jquery-3.6.0.min.js")
    js.append(base + "/user_files/assets/main.js")

    result = _old(self, body, css, js, head)
    return result

# add hook via monkey patching for anki < 2.1.20
# details here: https://addon-docs.ankiweb.net/monkey-patching.html
if is_old_anki():
    AnkiWebView.stdHtml = wrap(AnkiWebView.stdHtml, addForgettingAssets, "around")


# # # register hook
# gui_hooks.webview_will_set_content.append(on_webview_will_set_content)

def has_color(note):
    return "color" in note.keys()

def is_gradient_color(note):
    return has_color(note) and ("gradient" in note['color'])

def is_random(note):
    return has_color(note) and ('random' == note['color'])

def is_random_gradient(note):
    return has_color(note) and ('random-gradient' == note['color'])


#
#
# gradient generator
#
#

GRADIENT_FORMS = ['closest-side',
                  'circle',
                  'ellipse',
                  'closest-corner',
                  'farthest-side',
                  'farthest-corner']

def mk_random_position():
    return f"{random.choice(range(0, 100))}%"

# generate gradient

def mk_random_color(alpha=1):
    "generate random color"
    # red = random.choice(range(0, 255))
    # green = random.choice(range(0, 255))
    # blue = random.choice(range(0, 255))

    # return f"rgba({red}, {green}, {blue}, {alpha})"

    hue = random.choice(range(0, 360))
    saturation = random.choice(range(20, 80))
    lightness = random.choice(range(50, 80))

    return f"hsla({hue}, {saturation}%, {lightness}%, {alpha})"

def mk_random_gradient():
    form = random.choice(GRADIENT_FORMS)
    position_x = mk_random_position()
    position_y = mk_random_position()
    first_color = mk_random_color(random.random())
    second_color = mk_random_color(random.random())

    return f"radial-gradient({form} at {position_x} {position_y}, {first_color} 0%, {second_color} 100%)"

def mk_random_gradients(num):
    gradients = [mk_random_gradient() for x in range(num)]

    return ", ".join(gradients)

def inject_gradient(output, context):
    if not has_color(context.note()):
        stderr.write('no color field!\n')
        return

    color = context.note()['color']
    # bkg_field = 'background-color'

    # force random
    bkg_field = 'background'
    color = mk_random_gradients(random.choice(range(1, 4)))

    if is_gradient_color(context.note()):
        bkg_field = 'background'
        color = color.replace("<code>", '').replace("</code>", '')

    output.question_text = f"<style>.forgetting {{ {bkg_field}: {color}; }}</style>" + output.question_text
    output.answer_text += f"<style>.forgetting {{ {bkg_field}: {color}; }}</style>"


#
# modify play button
#
def has_play_button(content):
    return 'replay-button' in content

def random_eye_path():
    eye_num = random.choice(range(1, 6))       # num of eyes
    return base + f"/assets/images/eye-0{eye_num}.gif"


def inject_eye(output, context):
    # to the question
    # if not has_play_button(output.question_text):
    #     stderr.write("no play button: " + output.question_text)
    #     return

    eye_path = random_eye_path()

    # soup = BeautifulSoup(output.question_text)
    # for svg in soup.findAll(".playImage"):
    #     img = Tag(soup, 'img')
    #     svg.replaceWith(img)

    # output.question_text = str(soup)

    injection = f"<script>(function() {{ injectEyes('{eye_path}');}})();</script>"
    output.question_text += injection
    output.answer_text += injection

#
# hook
#
def on_card_did_render(output, context):
    inject_gradient(output, context)
    inject_eye(output, context)

# register our function to be called when the hook fires
# hooks.card_did_render.append(on_card_did_render)
