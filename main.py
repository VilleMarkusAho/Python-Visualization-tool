import os
from lib.GUI.toolbar import OpenFileButton
import matplotlib as mpl  # pip install matplotlib==3.5.1
import matplotlib.pyplot as plt
# Also, install openpyxl package with 'pip install openpyxl'.

mpl.rcParams["toolbar"] = 'toolmanager'
mpl.use('Qt5Agg')  # pip install PyQt5

print(mpl.__version__)

fig, ax = plt.subplots()

# chart configurations
ax.grid()

# window configurations
manager = plt.get_current_fig_manager()
manager.window.showMaximized()
manager.set_window_title('Visualization tool')

# adds custom button to the toolbar
tm = fig.canvas.manager.toolmanager
tm.add_tool('openfile', OpenFileButton, plot=ax, figure=fig, toolbar=manager.canvas.manager.toolbar)
button = tm.get_tool('openfile')
# button.image = str(Path('assets/excel-icon.svg').absolute())  # Sets icon to the button
button.image = "{0}/assets/excel-icon.svg".format(os.getcwd())
manager.canvas.manager.toolbar.add_tool(button, 'toolgroup')  # adds button to the toolbar

# removes unwanted navigation toolbar buttons
tm.remove_tool('subplots')
tm.remove_tool('help')
# tm.remove_tool('back')
# tm.remove_tool('forward')
# tm.remove_tool('home')

# shortcut configurations
tm.update_keymap('zoom', 'x')

plt.show()  # Display all open figures
