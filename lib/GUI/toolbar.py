import mplcursors  # pip install git+https://github.com/anntzer/mplcursors
import pandas as pd  # pip install pandas
# import matplotlib.pyplot as plt
from matplotlib.backend_tools import ToolToggleBase
# from matplotlib.widgets import Button as mpl_button
from lib.GUI.readfile import *


# Custom toolbar button
class OpenFileButton(ToolToggleBase):
    description = 'Choose excel file to read'

    def __init__(self, *args, figure, plot, toolbar, **kwargs):
        self.toolbar = toolbar
        self.fig = figure
        self.plot = plot
        super().__init__(*args, **kwargs)

    def trigger(self, *args, **kwargs):
        open_file(self.fig, self.plot, self.toolbar)


def open_file(fig, plot, toolbar):
    url = filepath()

    if url != '':
        sheets = get_sheets(url)

        # if len(sheets) == 1:
        draw_plot(fig, plot, toolbar, url, sheets[0])
        # else:
        # sheet = select_sheet(sheets)
        # draw_plot(fig, plot, toolbar, url, sheet)


# Executed when OpenFileButton is pressed
# Used to draw lines and configure charts
def draw_plot(fig, plot, toolbar, url, sheet):
    # clear axis
    plot.clear()

    # Converts excel file into dataframe
    df = pd.read_excel(url, sheet_name=sheet, engine='openpyxl')  # openpyxl engine is needed for reading
    # .xlsx excel files
    empty_cols = [col for col in df.columns if df[col].isnull().all()]  # Find the columns where each value is null (
    # empty columns)
    df.drop(empty_cols, axis=1, inplace=True)  # Drops the columns where value is null

    # Sets file name as a chart title
    title = os.path.basename(url)
    plot.set_title(os.path.splitext(title)[0])

    # Reads first and second cells on the first line of the dataframe
    plot.set_xlabel(df.iloc[:, 0].name)  # x-axis title
    plot.set_ylabel(df.iloc[:, 1].name)  # y-axis title

    count = 1  # Tracks the plot line count
    lines = []

    # Converts every row in each column into array
    try:
        for i in range(0, len(df.columns), 2):
            x = df.iloc[:, i]
            y = df.iloc[:, i + 1]

            line, = plot.plot(x, y, label=f'Line {count}')
            lines.append(line)
            count += 1

    except IndexError:
        error_message('Index out of range ERROR', 'Excel taulukosta puuttuu sarake')
        return
    except ValueError:
        error_message('Invalid value ERROR', 'Sarakkeiden rivit sisältävät huonoja arvoja')
        return

    # Legend info configurations
    leg = plot.legend(bbox_to_anchor=(1.12, 1), loc='upper right', fancybox=True, shadow=True, title='Click to '
                                                                                                     'toggle\n   line'
                                                                                                     ' on/off\n')

    lined = dict()
    for legline, origline in zip(leg.get_lines(), lines):
        legline.set_picker(5)  # 5 pts tolerance
        lined[legline] = origline

    # Event triggered when clicking legend lines
    def onpick(event):
        # on the pick event, find the original line corresponding to the
        # legend proxy line, and toggle the visibility
        try:
            legline = event.artist
            origline = lined[legline]
            vis = not origline.get_visible()
            origline.set_visible(vis)
            # Change the alpha on the line in the legend so we can see what lines
            # have been toggled
            if vis:
                legline.set_alpha(1.0)
            else:
                legline.set_alpha(0.2)
            fig.canvas.draw()
        except KeyError:
            pass

    fig.canvas.mpl_connect('pick_event', onpick)

    # adds grid to the canvas
    plot.grid()

    # adds tooltip to the cursor
    tooltip = mplcursors.cursor(plot, hover=2)  # shows information about artist when hovering the cursor over it
    marker = mplcursors.cursor(plot, multiple=True)  # this tooltip is used for setting markers to the plot lines

    # tooltip configurations
    @tooltip.connect("add")
    def _(sel):
        sel.annotation.get_bbox_patch().set(fc="white", alpha=1)  # Sets background color of tooltips
        # sel.annotation.arrow_patch.set(alpha=0)  # Makes tooltip arrow transparent
        sel.annotation.set_text(  # Information showed in the tooltip

            # shows values in three decimal accuracy
            f'{sel.artist.get_label()}\n{df.iloc[:, 1].name.strip()}: {sel.annotation.xy[1]:.10f}'
            f'\n{df.iloc[:, 0].name.strip()}: {sel.annotation.xy[0]:.3f}')

    # second tooltip configurations
    @marker.connect("add")
    def _(sel):
        sel.annotation.get_bbox_patch().set(fc="white", alpha=1)
        sel.annotation.set_text(
            f'{sel.artist.get_label()}\n{df.iloc[:, 1].name.strip()}: {sel.annotation.xy[1]:.10f}\n'
            f'{df.iloc[:, 0].name.strip()}: {sel.annotation.xy[0]:.3f}')

    fig.canvas.draw()

    toolbar.update()
    tm = fig.canvas.manager.toolmanager
    reset = tm.get_tool('viewpos')
    reset.clear(fig)
    reset.add_figure(fig)
    reset.push_current()
    reset.update_view()

    return True
