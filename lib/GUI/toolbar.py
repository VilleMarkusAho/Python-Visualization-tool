import mplcursors  # 'pip install git+https://github.com/anntzer/mplcursors'.
import pandas as pd  # 'pip install pandas'
from matplotlib.backend_tools import ToolToggleBase
from lib.GUI.readfile import *

# Custom toolbar button for reading excel files.
class OpenFileButton(ToolToggleBase):
    description = 'Choose excel file to read'
    
    def __init__(self, *args, figure, diagram, toolbar, **kwargs):
        self.toolbar = toolbar
        self.fig = figure
        self.diagram = diagram
        super().__init__(*args, **kwargs)
    
    def trigger(self, *args, **kwargs):
        # Executed when OpenFileButton is pressed.
        # Used to draw lines and configure charts.
        draw_plot(self.fig, self.diagram, self.toolbar)


def draw_plot(fig, diagram, toolbar):

    url = filepath()

    if url != '':
        # clear axis.
        diagram.clear()

        # Converts excel file into dataframe.
        # openpyxl engine is needed for reading.
        # .xlsx excel files
        df = pd.read_excel(url, engine='openpyxl')

        # Finds the columns where each value is null
        # (=empty columns).
        empty_cols = [col for col in df.columns if df[col].isnull().all()]

        # Drops the columns where value is null.
        df.drop(empty_cols, axis=1, inplace=True)

        # Sets file name as a chart title.
        title = os.path.basename(url)
        diagram.set_title(os.path.splitext(title)[0])

        # Reads first and second cells on the first line
        # of the dataframe.
        # x-axis title.
        diagram.set_xlabel(df.iloc[:, 0].name)

        # y-axis title.
        diagram.set_ylabel(df.iloc[:, 1].name)

        count = 1  # Tracks the plot line count
        lines = []

        # Converts every row in each column into array
        try:
            for i in range(0, len(df.columns), 2):
                x = df.iloc[:, i]
                y = df.iloc[:, i + 1]

                line, = diagram.plot(x, y, label=f'Line {count}')
                lines.append(line)
                count += 1

        except IndexError:
            error_message('Index out of range ERROR',
            'Excel taulukosta puuttuu sarake')
            return

        except ValueError:
            error_message('Invalid value ERROR',
            'Sarakkeiden rivit sisältävät huonoja arvoja')
        return
 
    # Legend info configurations
    leg = diagram.legend(bbox_to_anchor=(1.12, 1), loc='upper right', fancybox=True, shadow=True, title='Click to toggle\n line on/off\n')
    lined = dict()

    for legline, origline in zip(leg.get_lines(), lines):
        legline.set_picker(5) # 5 pts tolerance
        lined[legline] = origline

    # Event triggered when clicking legend lines.
    def onpick(event):
        # on the pick event, find the original line
        # corresponding to the legend proxy line,
        # and toggle the visibility.
        try:
            legline = event.artist
            origline = lined[legline]
            vis = not origline.get_visible()
            origline.set_visible(vis)

            # Change the alpha on the line in the
            # legend so we can see what lines have
            # been toggled.
            if vis:
                legline.set_alpha(1.0)
            else:
                legline.set_alpha(0.2)
                fig.canvas.draw()
                
        except KeyError:
            pass
    
    fig.canvas.mpl_connect('pick_event', onpick)

    # adds grid to the canvas.
    diagram.grid()

    # adds tooltip to the cursor.
    # tooltip shows information about artist when
    # hovering the cursor over it.
    tooltip = mplcursors.cursor(diagram, hover=2)
 
    # this tooltip is used for setting markers to the
    # plot lines.
    marker = mplcursors.cursor(diagram, multiple=True)
 
    # tooltip configurations
    @tooltip.connect("add")
    def _(sel):
        # Sets background color of tooltips.
        sel.annotation.get_bbox_patch().set(fc="white", alpha=1)
        # Information showed in the tooltip.
        sel.annotation.set_text(
        # shows values in 10 and 3 decimal
        # accuracy.
        f'{sel.artist.get_label()}\n'
        f'{df.iloc[:, 1].name.strip()}:'
        f' {sel.annotation.xy[1]:.10f}'
        f'\n{df.iloc[:, 0].name.strip()}:'
        f' {sel.annotation.xy[0]:.3f}')

    # second tooltip for tagging points of the plot.
    @marker.connect("add")
    def _(sel):
        sel.annotation.get_bbox_patch().set(fc="white", alpha=1)
        sel.annotation.set_text(
        f'{sel.artist.get_label()}\n'
        f'{df.iloc[:, 1].name.strip()}:'
        f' {sel.annotation.xy[1]:.10f}\n'
        f'{df.iloc[:, 0].name.strip()}:'
        f' {sel.annotation.xy[0]:.3f}')

    fig.canvas.draw()

    # functions below is for resetting view
    # positions memory stack
    toolbar.update()
    tm = fig.canvas.manager.toolmanager
    reset = tm.get_tool('viewpos')
    reset.clear(fig)
    reset.add_figure(fig)
    reset.push_current()
    reset.update_view()
