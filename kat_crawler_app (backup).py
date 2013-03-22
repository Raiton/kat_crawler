#!/usr/bin/env python
import gobject
import gtk
import appindicator
import lxml.etree
import os

 
def menuitem_response(w, buf):
  if buf=='Quit':
    gtk.main_quit()
  elif buf=='Refresh':
    perform()
    gtk.main_quit()


def perform():
  if os.path.exists('/home/raiton/kat/kat_last_tv_shows.xml'):
    os.system('cd /home/raiton/kat;rm kat_last_tv_shows.xml')
  os.system('cd /home/raiton/kat;scrapy crawl kat_crawler -o kat_last_tv_shows.xml -t xml')

  if os.path.exists('/home/raiton/kat/kat_last_tv_shows.xml'):
    tree = lxml.etree.parse('/home/raiton/kat/kat_last_tv_shows.xml')
  else:
    tree=''
  entries=tree.xpath("//name/value")
  

 
  menu_items=[]
  menu=gtk.Menu()
   #Refresh part
  menu_items = gtk.MenuItem('Refresh')
  menu.append(menu_items)
  menu_items.connect("activate", menuitem_response, 'Refresh')
  menu_items.show()
  #end Refresh part

  # create some
  for entry in entries:
    buf = entry.text
    menu_items = gtk.MenuItem(buf)
    menu.append(menu_items)

    # this is where you would connect your menu item up with a function:
 
    menu_items.connect("activate", menuitem_response, buf)
 
    # show the items
    menu_items.show()
  
  #quit part
  menu_items = gtk.MenuItem('Quit')
  menu.append(menu_items)
  menu_items.connect("activate", menuitem_response, 'Quit')
  menu_items.show()
  #end quit part

  ind.set_menu(menu)
  ind.set_icon("ubuntuone-client-idle")

 
  gtk.main()


if __name__ == "__main__":
  ind = appindicator.Indicator ("example-simple-client",
                              "indicator-messages",
                              appindicator.CATEGORY_APPLICATION_STATUS)
  ind.set_status (appindicator.STATUS_ACTIVE)
  ind.set_attention_icon ("indicator-messages-new")
 
  # create a menu
  menu = gtk.Menu()
  perform()