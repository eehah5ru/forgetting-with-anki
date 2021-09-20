from sys import stderr, stdout
from anki import hooks
from anki.template import TemplateRenderContext, TemplateRenderOutput
import aqt
from aqt import gui_hooks
from aqt import mw
import random

# inject css
# https://github.com/ShoroukAziz/Beautify-Anki/blob/master/__init__.py
#
# webview hook:
# see details: https://github.com/ankitects/anki/blob/main/qt/tools/genhooks_gui.py
# def on_webview_will_set_content(web_content: aqt.webview.WebContent,
#                                 context):
#     if not isinstance(context, aqt.reviewer.Reviewer):
#         # not reviewer, do not modify content
#         return

#     # reviewer, perform changes to content
#     context: aqt.reviewer.Reviewer

#     note = mw.reviewer.card.note()
#     if 'color' in note.keys():
#         color = note['color']
#         web_content.head += f"<style>.card {{ background-color: {color}; }}</style>"
#         stderr.write(web_content.body)
#     # web_content.body += f"<style>.card {{ background-color: cyan; }}</style>"

# # register hook
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

#
# hook
#
def on_card_did_render(output: TemplateRenderOutput, context: TemplateRenderContext):
    # # let's uppercase the characters of the front text
    # output.question_text = output.question_text.upper()

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


# register our function to be called when the hook fires
hooks.card_did_render.append(on_card_did_render)
