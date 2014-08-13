
'''
    use bardeen's MPL class to save figures for use in reports
    function should:
    - import subplots & show from mympl
    - preferably use 'label' argument to subplots that are to be saved
        (otherwise numbers can be used, but that is sensitive to change)
    - call show() in __main__ (so it's not used when imported)
'''

from bardeen.mpl.xkcd import xkcdMPL as MPL, close, show, subplots
from numpy import linspace
from numpy.random import rand


''' initialize '''
directory = './'
mpl = MPL.instance(extension = ['png', 'pgf'], directory = '.', save_all = False)
properties =  {
    'max_width': 6.17,
    'dpi': 600,
    'font_name': 'cmr10',
    'font_size': 10.0,
    'font_weight': 'normal',
    'font_style': 'normal',
}

mpl.order(label = 'demo_image', filename = 'demo', **properties)
fig, axi = subplots(total = 4, label = 'demo_image', save_dpi = 80)
for k, ax in enumerate(axi):
    ax.scatter(linspace(0, 100, 101), linspace(0, 100, 101) + 15 * rand(101), label = 'line %d.1' % k)
    ax.scatter(linspace(0, 100, 101), 100 - linspace(0, 100, 101) + 5 * rand(101), label = 'line %d.2' % k)
    ax.scatter(linspace(0, 100, 101), 50 + .5 * abs(linspace(0, 100, 101) - 50) * (rand(101) * 2 - 1), label = 'line %d.3' % k)
    ax.set_xlabel('something ($\\frac{A}{b}$)')
    ax.set_ylabel('another thing ($q^{2}_{%d}$)' % k)
    ax.legend()

fig, ax = subplots(total = 1, label = 'unordered_demo')
for k in range(7):
    ax.plot(linspace(0, 100, 101) + 15 * rand(101), label = 'label%d' % k)
ax.set_xlabel('something ($\\frac{A}{b}$)')
ax.set_ylabel('another thing ($q^{2}_{%d}$)' % k)
ax.legend()

close()


