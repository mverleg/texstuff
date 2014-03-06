
'''
    replacements for axis methods (labels, colours)
'''

''' default color cycle for scatter '''
boynton_colors = [
    (0., 0., 1., 1.),    # Blue
    (1., 0., 0., 1.),    # Red
    (0., 1., 0., 1.),    # Green
    (1., 1., 0., 1.),    # Yellow
    (1., 0., 1., 1.),    # Magenta
    (1., .5, .5, 1.),    # Pink
    (.5, .5, .5, 1.),    # Gray
    (.5, 0., 0., 1.),    # Brown
    (1., .5, 0., 1.),    # Orange
]

''' new ax.scatter method that cycles through colours if none are provided '''
def color_cycle_scatter(ax, *args, **kwargs):
    if 'color' in kwargs.keys():
        return ax.mono_color_scatter(*args, **kwargs)
    return ax.mono_color_scatter(*args, color = next(ax.custom_color_cycle), **kwargs)

''' new ax.xlabel with smaller default padding (not a rcParam apparently) '''
def small_pad_xlabel(ax, *args, **kwargs):
    if 'labelpad' in kwargs.keys():
        return ax.big_pad_xlabel(*args, **kwargs)
    return ax.big_pad_xlabel(*args, labelpad = 0., **kwargs)
def small_pad_ylabel(ax, *args, **kwargs):
    if 'labelpad' in kwargs.keys():
        return ax.big_pad_ylabel(*args, **kwargs)
    return ax.big_pad_ylabel(*args, labelpad = 2., **kwargs)


