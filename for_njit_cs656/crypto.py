from big_ol_pile_of_manim_imports import *

from hashlib import sha256
import binascii

#force_skipping
#revert_to_original_skipping_status

BITCOIN_COLOR = "#f7931a"

def get_cursive_name(name):
    result = TextMobject("\\normalfont\\calligra %s"%name)
    result.set_stroke(width = 0.5)
    return result

def sha256_bit_string(message):
    hexdigest = sha256(message.encode('utf-8')).hexdigest()
    return bin(int(hexdigest, 16))[2:]

def bit_string_to_mobject(bit_string):
    line = TexMobject("0"*32)
    pre_result = VGroup(*[
        line.copy() for row in range(8)
    ])
    pre_result.arrange_submobjects(DOWN, buff = SMALL_BUFF)
    result = VGroup(*it.chain(*pre_result))
    result.scale(0.7)
    bit_string = (256 - len(bit_string))*"0" + bit_string

    for i, (bit, part) in enumerate(zip(bit_string, result)):
        if bit == "1":
            one = TexMobject("1")[0]
            one.replace(part, dim_to_match = 1)
            result.submobjects[i] = one

    return result

def sha256_tex_mob(message, n_forced_start_zeros = 0):
    true_bit_string = sha256_bit_string(message)
    n = n_forced_start_zeros
    bit_string = "0"*n + true_bit_string[n:]
    return bit_string_to_mobject(bit_string)

class EthereumLogo(SVGMobject):
    CONFIG = {
        "file_name" : "ethereum_logo",
        "stroke_width" : 0,
        "fill_opacity" : 1,
        "color_chars" : "8B8B48",
        "height" : 0.5,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        for part, char in zip(self.submobjects, self.color_chars):
            part.set_color("#" + 6*char)

class LitecoinLogo(SVGMobject):
    CONFIG = {
        "file_name" : "litecoin_logo",
        "stroke_width" : 0,
        "fill_opacity" : 1,
        "fill_color" : LIGHT_GREY,
        "height" : 0.5,
    }

class TenDollarBill(VGroup):
    CONFIG = {
        "color" : GREEN,
        "height" : 0.5,
        "mark_paths_closed" : False,
    }
    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)
        rect = Rectangle(
            height = 2.61,
            width = 6.14,
            color = self.color,
            mark_paths_closed = False,
            fill_color = BLACK,
            fill_opacity = 1,
        )
        rect.set_height(self.height)
        oval = Circle()
        oval.stretch_to_fit_height(0.7*self.height)
        oval.stretch_to_fit_width(0.4*self.height)
        rect.add_subpath(oval.points)

        pi = Randolph(
            mode = "pondering",
            color = GREEN_B
        )
        pi.set_width(oval.get_width())
        pi.move_to(oval)
        pi.shift(0.1*pi.get_height()*DOWN)

        self.add(pi, rect)
        for vect in UP+LEFT, DOWN+RIGHT:
            ten = TexMobject("\\$10")
            ten.set_height(0.25*self.height)
            ten.next_to(self.get_corner(vect), -vect, SMALL_BUFF)
            ten.set_color(GREEN_C)
            self.add(ten)


##################

class AskQuestion(Scene):
    CONFIG = {
        "time_per_char" : 0.06,
    }
    def construct(self):
        bit_logo = BitcoinLogo()
        eth_logo = EthereumLogo()

        strings = [
            "Can ", "we ", "change ", "a ", 
            "Bitcoin     ", "video ", "to     ", "Ethereum", "?"
        ]
        question = TextMobject(*strings)
        question.set_color_by_tex("Bitcoin", YELLOW)
        question.set_color_by_tex("Ethereum", YELLOW)

        bit_logo.to_corner(UP + LEFT)
        bit_logo.scale(2.)
        eth_logo.to_corner(UP + RIGHT, buff=MED_LARGE_BUFF)
        eth_logo.scale(3.)
        arrow = Arrow(bit_logo.get_corner(RIGHT), eth_logo.get_corner(LEFT))

        self.wait()
        for word, part in zip(strings, question):
            n_chars = len(word.strip())
            n_spaces = len(word) - n_chars
            self.play(
                LaggedStart(FadeIn, part),
                run_time = self.time_per_char * len(word),
                rate_func = squish_rate_func(smooth, 0, 0.5)
            )
            if word.strip() == "Bitcoin":
                self.play(DrawBorderThenFill(bit_logo))
            elif word.strip() == "Ethereum":
                self.play(DrawBorderThenFill(eth_logo))
            elif word.strip() == "to":
                self.play(ShowCreation(arrow))

            self.wait(self.time_per_char*n_spaces)

        self.wait(2)

