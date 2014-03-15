
'''
    change matplotlib plotting functions a little to make saving 
    images easier and fix minor nuicances
    - subplots returns one list of axis objects rather than a list of lists
    - closing one figure will close all the figures
    - make tight layout the default
    !! saving stuff
'''

import matplotlib
from matplotlib.pyplot import subplots as mpl_subplots
from matplotlib.pyplot import figure as mpl_figure
from matplotlib.pyplot import show as mpl_show
from matplotlib.pyplot import close as mpl_close
from itertools import cycle
from numpy import array, concatenate, ndarray
from re import compile
from os.path import join
from types import MethodType, StringTypes
#from settings import image_dir
from mympl_ax import boynton_colors, color_cycle_scatter, small_pad_xlabel, small_pad_ylabel
from mympl_order import MPLorder
from collections import defaultdict


'''
    Singleton class that keeps track of figures
'''
class MyMPL(object):
    
    ''' max_width, overriden by order if there is one '''
    max_width = 6.17
    
    ''' extension may also be a list of extensions '''
    def __init__(self, save_all = False, extension = 'png', directory = '.'):
        
        ''' operation settings '''
        self.save_all = save_all
        self.directory = directory
        if isinstance(extension, StringTypes):
            self.default_extension = [extension]
        else:
            self.default_extension = extension
        
        ''' pgf backend settings '''
        matplotlib.rcParams['text.latex.unicode'] = True
        matplotlib.rcParams['text.usetex'] = True
        matplotlib.rcParams['pgf.texsystem'] = 'pdflatex'
        
        ''' register single instance '''
        try:
            self.__class__.single_instance
        except AttributeError:
            ''' no instance yet; good! '''
            self.__class__.single_instance = self
        else:
            ''' an instance already exists! '''
            raise Exception('%s already has an instance!' % self.__class__)
        ''' initial variables '''
        self.all_figures = []
        self.orders = defaultdict(list)
    
    def default_font_properties(self):
        return {
            'family': 'cmr10',
            'size': 10.0,
            'weight': 'normal',
            'style': 'normal',
        }
    
    ''' get the singleton instance '''
    @classmethod
    def instance(cls, *args, **kwargs):
        try:
            cls.single_instance
        except AttributeError:
            cls.single_instance = cls(*args, **kwargs)
        return cls.single_instance
    
    ''' better subplots function '''
    def subplots(self, ver = 1, hor = 1, label = None, figsize = (None, None), tight_layout = True, show_toolbar = False, total = None, dpi = 120, save_dpi = 300, *args, **kwargs):
        ''' create tiles if total set '''
        if total is not None:
            hor = ver = int(total ** 0.5)
            if hor * ver < total:
                hor += 1
            if hor * ver < total:
                ver += 1
        ''' if this figure has been ordered, change a few properties '''
        if label is None:
            label = 'fig_%d' % len(self.all_figures)
        max_width = self.max_width
        font_func = self.default_font_properties
        if label in self.orders.keys():
            for order in self.orders[label]:
                ''' change font properties everywhere '''
                font_func = order.font_properties
                max_width = order.max_width
                ''' change dpi '''
                save_dpi = order.dpi
        ''' change font properties everywhere '''
        matplotlib.rc('font', **font_func())
        if figsize[0] is None:
            ''' default figure size is 'maximal' '''
            figsize = (max_width, 0.75 * max_width)
        elif figsize[0] > max_width:
            ''' scale down figure if too large '''
            scale = max_width / figsize[0]
            figsize = (max_width, scale * figsize[1])
        disp_dpi = dpi
        ''' hide toolbar unless otherwise specified '''
        matplotlib.rcParams['toolbar'] = 'None'
        ''' fix a bug with minus sign not showing '''
        matplotlib.rcParams['axes.unicode_minus'] = False
        ''' change the default color cycle '''
        matplotlib.rcParams['axes.color_cycle'] = boynton_colors
        ''' change legend to make it smaller '''
        matplotlib.rcParams['legend.labelspacing'] = .2
        matplotlib.rcParams['legend.borderpad'] = 0.3
        ''' the actual figure '''
        if hor <= 0 or ver <= 0:
            ''' create empty figure if no subplots requested '''
            fig = mpl_figure(figsize = figsize, dpi = disp_dpi, *args, **kwargs)
            axi = array([])
        else:
            ''' create the requested subplots '''
            fig, axi = mpl_subplots(ver, hor, figsize = figsize, dpi = disp_dpi, *args, **kwargs)
            ''' tight layout unless otherwise specified '''
            if tight_layout:
                fig.tight_layout(rect = [.045, .03, 1., 1.], pad = .1, w_pad = 2., h_pad = 1.)
            ''' merge axi into one list instead of sublists '''
            try:
                axi = concatenate(axi)
            except ValueError:
                ''' axi is already one list (hor = 1 probably) '''
            except TypeError:
                ''' axi is a single object (hor = ver = 1 probably) '''
            ''' remove extra axi if 'total' used '''
            if total is not None and total != 1:
                for ax in axi[total:]:
                    ax.axis('off')
                axi = axi[:total]
        ''' store dpi for saving '''
        fig.save_dpi = save_dpi
        ''' override ax.methods '''
        for ax in (axi if isinstance(axi, ndarray) else [axi]):
            ''' override scatter to use color cycle '''
            ax.custom_color_cycle = cycle(boynton_colors)
            ax.mono_color_scatter = ax.scatter
            ax.scatter = MethodType(color_cycle_scatter, ax, ax.__class__)
            ''' label distances '''
            ax.big_pad_xlabel = ax.set_xlabel
            ax.set_xlabel = MethodType(small_pad_xlabel, ax, ax.__class__)
            ax.big_pad_ylabel = ax.set_ylabel
            ax.set_ylabel = MethodType(small_pad_ylabel, ax, ax.__class__)
        ''' change some things if this image was ordered '''
        fig.label = label
        for order in self.orders[label]:
            order.figure = fig
        fig.canvas.set_window_title(label)
        ''' store figure reference '''
        self.all_figures.append(fig)
        ''' return '''
        return (fig, axi) if axi is not None else fig
    
    ''' better figure function '''
    def figure(self, *args, **kwargs):
        return self.subplots(ver = 0, hor = 0, *args, **kwargs)[0]
    
    ''' better show function '''
    ''' you can pass callbacks to call after showing, to have sort of 'non-blocking' behaviour 
        use functools.partial if you want to supply any arguments '''
    def show(self, callbacks = [], close_immediately = False, *args, **kwargs):
        for fig in self.all_figures:
            ''' save the figure if it has been ordered '''
            filenames = []
            if len(self.orders[fig.label]):
                ''' has this figure been ordered? '''
                for order in self.orders[fig.label]:
                    if compile('^(.*[^\./])\.\w+$').match(order.filename):
                        ''' already has an extension '''
                        filenames.append(order.filename)
                    else:
                        ''' no extension; add all '''
                        filenames.extend('%s.%s' % (order.filename, extension) for extension in self.default_extension)
                ''' order fulfilled; remove it '''
                del self.orders[fig.label]
            elif self.save_all:
                ''' there is no filename (just a label), so add all extensions to that and treat it like a filename '''
                filenames.extend('%s.%s' % (fig.label, extension) for extension in self.default_extension)
            if filenames:
                print 'saving \'%s\' as %s' % (fig.label, ', '.join('\'%s\'' % filename for filename in filenames))
            for filename in filenames:
                filename = join(self.directory, filename)
                fig.savefig(filename, dpi = fig.save_dpi)
        for fig in self.all_figures:
            ''' attach the on-close handles to close all other figures too '''
            fig.canvas.mpl_connect('close_event', self.close_all)
            ''' close immediately if close is requested '''
            if close_immediately:
                fig.canvas.mpl_connect('draw_event', self.close_all)
            ''' show the figure '''
            fig.show(*args, **kwargs)
        ''' any unsaved figures? '''
        remaining_orders = sum(self.orders.values(), [])
        if len(remaining_orders):
            print 'there are %d unsaved orders! figures were not found for:' % len(remaining_orders)
            for order in remaining_orders:
                print '\'%s\' (\'%s\')' % (order.label, order.filename)
        ''' show all figures to prevent error '''
        mpl_show()
    
    def close(self, callbacks = [], *args, **kwargs):
        self.show(callbacks = callbacks, close_immediately = True, *args, **kwargs)
    
    ''' tell MyMPL to save a figure if it occurs in the future '''
    def order(self, label, filename = None, **kwargs):
        if filename is None:
            filename = label
        self.orders[label].append(MPLorder(label, filename, **kwargs))
    
    ''' close all figures '''
    @staticmethod
    def close_all(event):
        for fig in MyMPL.instance().all_figures:
            mpl_close(fig)
        MyMPL.instance().all_figures = []



''' non-class version like the normal MPL '''
def figure(*args, **kwargs):
    return MyMPL.instance().figure(*args, **kwargs)

def subplots(*args, **kwargs):
    return MyMPL.instance().subplots(*args, **kwargs)

def show(*args, **kwargs):
    return MyMPL.instance().show(*args, **kwargs)

''' opens and immediately closes figures; use instead of show (is already open use close_all) '''
def close(*args, **kwargs):
    return MyMPL.instance().close(*args, **kwargs)

def order(*args, **kwargs):
    MyMPL.instance().order(*args, **kwargs)

