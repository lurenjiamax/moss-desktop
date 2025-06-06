from typing import TYPE_CHECKING, Dict

import pygameextra as pe

from gui import APP_NAME
from gui.i18n import i18n
from .settings_menu import SettingsSidebarChain, BackButton, parse_menu_xml
from .settings_view import SettingsView
from ...defaults import Defaults
from ...events import ResizeEvent

if TYPE_CHECKING:
    from gui import GUI
    from gui.aspect_ratio import Ratios
    from rm_api import API


class Settings(pe.ChildContext):
    LAYER = pe.AFTER_LOOP_LAYER
    MENUS = [
        {
            'text': f'{APP_NAME} Settings',
            'icon': 'moss',
            'action': 'moss',
            'data': 'xml_settings',
        }
    ]

    # definitions from GUI
    api: 'API'
    parent_context: 'GUI'
    icons: Dict[str, pe.Image]
    ratios: 'Ratios'

    def __init__(self, parent: 'GUI'):
        super().__init__(parent)
        self.sidebar = SettingsSidebarChain(self)
        print(self.data.keys())
        print(f'xml_settings/{i18n.get_locale()}/default')

        self.xml_interactor = SettingsView(self, parse_menu_xml(self.data.get(f'xml_settings/{i18n.get_locale()}/default'))[0], self)
        self.back_button = BackButton(self)
        self.api.add_hook('settings_resize_check', self.handle_resize_event)

    def handle_resize_event(self, event):
        if isinstance(event, ResizeEvent):
            self.sidebar.handle_resize()
            self.xml_interactor.handle_resize()

    def loop(self):
        # Display the back button
        self.back_button()
        self.sidebar()
        self.xml_interactor()

    def post_loop(self):
        # Draw a separator line between the sidebar and the settings menu
        pe.draw.line(
            Defaults.OUTLINE_COLOR,
            (0, self.ratios.main_menu_top_height),
            (self.ratios.main_menu_side_bar_width, self.ratios.main_menu_top_height),
            w=self.ratios.line
        )

        # Outline the end of the Side bar
        pe.draw.line(
            Defaults.OUTLINE_COLOR,
            (self.ratios.main_menu_side_bar_width, 0),
            (self.ratios.main_menu_side_bar_width, self.height),
            w=self.ratios.line
        )

    def close(self):
        self.close_screen()

    def get(self, value):
        return self.config.get(value)

    def set(self, key, value, value_type):
        self.config[key] = value
        self.dirty_config = True
