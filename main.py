import matplotlib as mpl  # pip install matplotlib==3.5.1
import matplotlib.pyplot as plt
from lib.GUI.toolbar import OpenFileButton
import os
# Also, install openpyxl package with 'pip install openpyxl'.

mpl.rcParams["toolbar"] = 'toolmanager'
mpl.use('Qt5Agg')  # pip install PyQt5

print(mpl.__version__)

fig, ax = plt.subplots()

# chart configurations.

ax.grid()
# window configurations.
manager = plt.get_current_fig_manager()
manager.window.showMaximized()
manager.set_window_title('Visualization tool')

# adds custom button to the toolbar.
tm = fig.canvas.manager.toolmanager
toolbar = manager.canvas.manager.toolbar
tm.add_tool('openfile', OpenFileButton, diagram=ax,
            figure=fig, toolbar=toolbar)

button = tm.get_tool('openfile')
# Sets icon to the button.
button.image = "{0}/assets/excel-icon.svg".format(os.getcwd())
# adds button to the toolbar.
manager.canvas.manager.toolbar.add_tool(button, 'toolgroup')

# All toolbar default buttons are listed below, uncomment
# or add "#" without quote marks if you want to remove or
# add specific button.
tm.remove_tool('subplots')
tm.remove_tool('help')
# tm.remove_tool('back')
# tm.remove_tool('forward')
# tm.remove_tool('home')

# shortcut configurations.
tm.update_keymap('zoom', 'x')

plt.show()  # Display all open figures.
