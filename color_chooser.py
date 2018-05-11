# This application pick n hex colors that are most contrasting
import bokeh.palettes as palettes
import math as m


class ColorPicker:
    def __init__(self, n):
        self.n = n
        self.hex_palette = palettes.d3['Category20'][20]
        # self.hex_palette = palettes.colorblind['Colorblind'][8]
        self.baseline_color = self.hex_palette[5]

    def hex_to_rgm(self, hex):
        tran = hex.lstrip('#')
        return tuple(int(tran[i:i + 2], 16) for i in (0, 2, 4))

    def calc_color_difference(self, lhs, rhs):
        rl, gl, bl = lhs
        rr, gr, br = rhs
        distance = m.sqrt((rl-rr) ** 2 + (gl-gr) ** 2 + (bl-br) ** 2)
        return distance

    def log_loss(self, old_list, candidate):
        candidate = self.hex_to_rgm(candidate)
        sum = 0
        for color in old_list:
            color = self.hex_to_rgm(color)
            if self.calc_color_difference(color, candidate) > 0:
                sum += (m.log(self.calc_color_difference(color, candidate)))**2
            else:  # = 0, can not < 0
                sum += 0
        return sum

    def pick_colors(self):
        color_list = [self.baseline_color]

        def get_key(item):
            return item[-1]

        for i in range(self.n):
            loss_list = []
            for candidate in self.hex_palette:
                if candidate not in color_list:
                    loss = self.log_loss(color_list, candidate)
                    loss_list.append([candidate, loss])
            sorted_loss_list = list(sorted(loss_list, key=get_key, reverse=True))
            color_list.append(sorted_loss_list[0][0])
        return color_list


def main_color_chooser(n):
    color_chooser = ColorPicker(n-1)
    print(color_chooser.pick_colors())
    return color_chooser.pick_colors()


main_color_chooser(3)