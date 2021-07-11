#!/usr/bin/env python3
import os
import gi
gi.require_version("Gtk","3.0")
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = "Ad-blocker"
ICON = os.path.abspath('./icons/cubes.png')
print(ICON)

res = os.system("cat ./hosts/hosts_up/* > /etc/hosts")
if not res:
    print("--- Adaway host file activates at STARTUP")
else:
    print("--- Error occur, unable to activate hosts files at STARTUP")


class MyIndicator:

    def __init__(self):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID,ICON,appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        gtk.main()

    def build_menu(self):
        menu = gtk.Menu()

        activeBtn = gtk.RadioMenuItem(label="Active")
        activeBtn.set_active(True)
        activeBtn.connect("toggled", self.on_toggle_activeBtn)

        inactiveBtn = gtk.RadioMenuItem(label="Inactive", group=activeBtn)
        inactiveBtn.set_active(False)
        inactiveBtn.connect("toggled", self.on_toggle_inactiveBtn)

        quitBtn = gtk.MenuItem(label='Quit')
        quitBtn.connect('activate',self.quit_me)

        hostsBtn = gtk.MenuItem(label = 'Hosts Files')
        hostsBtn.connect('activate',self.show_hosts)

        separator = gtk.SeparatorMenuItem()

        menu.append(activeBtn)
        menu.append(inactiveBtn)
        menu.append(quitBtn)
        menu.append(separator)
        menu.append(hostsBtn)

        menu.show_all()
        return menu

    def on_toggle_activeBtn(self,radiobutton):
        if radiobutton.get_active():
            res = os.system("cat ./hosts/hosts_up/* > /etc/hosts")
            if not res:
                print("--- Adaway host file activated")
            else:
                print("--- Error occur, unable to activate Adaway hosts file")
        else:
            print("Toggled Off")

    def on_toggle_inactiveBtn(self,radiobutton):
        if radiobutton.get_active():
            res = os.system("cat ./hosts/hosts.ori > /etc/hosts")

            if not res:
                print("--- Adaway host file deactivated, set to dafault")
            else:
                print("--- Error occur, unable to deactivate Adaway hosts file")

        else:
            print("Toggled Off")

    def quit_me(self,source):
        res = os.system("cat ./hosts/hosts.ori > /etc/hosts")
        if not res:
            print("--- Host file set to default")
        else:
            print("--- Error occured while existing, hosts file not set to deafult")
        gtk.main_quit()

    def show_hosts(self,source):
        print("Show my hosts")

show_indicator = MyIndicator()
