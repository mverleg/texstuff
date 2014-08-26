
"""
	generate some demo images, as an example
"""

from bardeen.mpl import MPL, subplots, show
from numpy import linspace
from numpy.random import rand


def generate_demo_imgs():

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


if __name__ == '__main__':
	generate_demo_imgs()
	show()


