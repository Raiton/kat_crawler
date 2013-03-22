#!/usr/bin/env python
from gi.repository import Gtk,Gdk
from gi.repository import AppIndicator3 as appindicator
import lxml.etree
import os
from gi.repository import GLib
import datetime

now = datetime.datetime.now()

TIME_REFRESH_MINUTES=30
Last_Update=now.strftime("%d-%m-%Y %H:%M:%S")
def menuitem_response(w, buf):
  if buf=='Quit':
    Gtk.main_quit()
  elif buf=='Refresh':
    perform()
    Gtk.main_quit()
def timer_passed():
  perform()
  return True

def perform():
  global Last_Update
  ind.set_status (appindicator.IndicatorStatus.ATTENTION)

  if os.path.exists('/home/raiton/kat/kat_last_tv_shows.xml'):
    os.system('cd /home/raiton/kat;mv kat_last_tv_shows.xml kat_last_tv_shows.xml.backup')
  os.system('cd /home/raiton/kat;timeout 5 scrapy crawl kat_crawler --nolog  -o kat_last_tv_shows.xml -t xml')
    
  try:
    tree=lxml.etree.parse('/home/raiton/kat/kat_last_tv_shows.xml')
    now = datetime.datetime.now()
    Last_Update =now.strftime("%d-%m-%Y %H:%M:%S")
  except Exception:
    tree=lxml.etree.parse('/home/raiton/kat/kat_last_tv_shows.xml.backup')


  entries=tree.xpath("//name/value")
  
  ind.set_status (appindicator.IndicatorStatus.ACTIVE)

 
  menu_items=[]
  menu=Gtk.Menu()

   #Refresh part
  name_refresh_menu='Refresh ['+Last_Update+' ]'
  menu_items = Gtk.MenuItem(name_refresh_menu)
  menu.append(menu_items)
  menu_items.connect("activate", menuitem_response, 'Refresh')
  menu_items.show()
  #end Refresh part

  # create some
  for entry in entries:
    buf = entry.text
    menu_items = Gtk.MenuItem(buf)
    menu.append(menu_items)

    # this is where you would connect your menu item up with a function:
 
    menu_items.connect("activate", menuitem_response, buf)
 
    # show the items
    menu_items.show()
  
  #quit part
  menu_items = Gtk.MenuItem('Quit',name='into')
  # menu_items.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("green"))
  # print  menu_items.get_style().bg[Gtk.StateType.NORMAL]
  # # style = menu_items.get_style().copy ()
  # # style.bg[Gtk.StateType.NORMAL] = Gdk.color_parse('green')
  # # menu_items.set_style (style)


  menu.append(menu_items)
  menu_items.connect("activate", menuitem_response, 'Quit')
  menu_items.show()
  #end quit part

  ind.set_menu(menu)
  ind.set_icon("ubuntuone-client-idle")
  GLib.timeout_add_seconds(60*TIME_REFRESH_MINUTES, timer_passed)

  Gtk.main()


if __name__ == "__main__":
  ind = appindicator.Indicator.new("example-simple-client",
                              "indicator-messages",
                              appindicator.IndicatorCategory.APPLICATION_STATUS)
  ind.set_status (appindicator.IndicatorStatus.ACTIVE)
  ind.set_attention_icon ("ubuntuone-client-updating")

 
  # create a menu

  perform()