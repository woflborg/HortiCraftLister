#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZetCode wxPython tutorial

In this example we create review
layout with wx.FlexGridSizer.

author: Jan Bodnar
website: www.zetcode.com
last modified: April 2018
"""

import wx
import win32clipboard
import threading
import winsound
import re
import os.path
import json 


class HortiCraftLister(wx.Frame):

    def __init__(self, parent, title):
        super(HortiCraftLister, self).__init__(parent, title=title)
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.listbox = wx.ListBox(panel,style=wx.LB_EXTENDED)
        self.listboxContents = {}
        self.listBoxPrices = {}
        hbox.Add(self.listbox, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)

        

        btnPanel = wx.Panel(panel)
        vbox = wx.BoxSizer(wx.VERTICAL)
        addBtn = wx.Button(btnPanel, wx.ID_ANY, 'Export', size=(90, 30))
        remBtn = wx.Button(btnPanel, wx.ID_ANY, 'Remove', size=(90, 30))
        self.polBtn = wx.Button(btnPanel, wx.ID_ANY, 'Poll', size=(90, 30))
        self.price = wx.TextCtrl(btnPanel, wx.ID_ANY, value='', size=(90, 30))
        setPrice = wx.Button(btnPanel, wx.ID_ANY, 'Set Price', size=(90, 30))
        
        self.pollActive = False

        vbox.Add((-1, 20))
        vbox.Add(addBtn)
        vbox.Add(remBtn, 0, wx.TOP, 5)
        vbox.Add(self.polBtn, 0, wx.TOP, 5)
        vbox.Add(self.price, 0, wx.TOP, 5)
        vbox.Add(setPrice, 0, wx.TOP, 5)
        
        
        self.Bind(wx.EVT_BUTTON, self.OnExport, id=addBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=remBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnTogglePoll, id=self.polBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSetPrice, id=setPrice.GetId())

        btnPanel.SetSizer(vbox)
        hbox.Add(btnPanel, 0, wx.EXPAND | wx.RIGHT, 20)
        panel.SetSizer(hbox)

        self.LoadPrices()

        self.SetTitle('HortiCraftLister')
        self.Centre()
        
        
    def OnDelete(self, event):
        #RemoveItem
        sels = self.listbox.GetSelections()
        for sel in sels:
            if(sel > -1):
                text = self.GetActualCraftName(self.listbox.GetString(sel))
                for item in self.listboxContents:
                    if(text == item):
                         self.RemoveItem(item)
                         break
        self.UpdateListBoxGui()


    def GetActualCraftName(self, text):
        strip1 = text[3:text.find(" x")]
        strip2 = strip1[0:strip1.find("|")]
        strip3 = strip2.strip()
        return strip3
            
    def OnSetPrice(self, event):
        sels = self.listbox.GetSelections()
        newPrice = self.price.GetValue()
        for sel in sels:
            if(sel > -1):
                text = self.GetActualCraftName(self.listbox.GetString(sel))
                self.listBoxPrices[text] = newPrice
                #print(text)
        self.SavePrices()                
        self.UpdateListBoxGui()
        

    def OnExport(self, event):
        ret = []
        cats = self.OrderedCategories()
        for cat in cats:
            ret.append(""+cat+"" + ":")
            for item in sorted(cats[cat]):
                if(self.listboxContents[item] > 0):
                    itemName = "   " + item + " "
                    if(self.listboxContents[item] > 1):
                        itemName = itemName +"x" + str(self.listboxContents[item])
                    
                    if(item in self.listBoxPrices):
                        itemName = itemName +  " | " + str(self.listBoxPrices[item])

                        
                    ret.append(itemName)
            ret.append(" ")
        retstring = "\n".join(ret)
        self.SetClipBoardText(retstring)
        self.Boop()
        #print(retstring)

    def ProcessClipboardContents(self, data):
        lines = data.splitlines()
        if len(lines) > 6:
            self.AddNewItem(self.FixStupidNames(lines[7]))
        if len(lines) > 7:
            self.AddNewItem(self.FixStupidNames(lines[8]))
        if len(lines) > 8:
            self.AddNewItem(self.FixStupidNames(lines[9]))
        self.UpdateListBoxGui()


    def AddNewItem(self, item):
        if item in self.listboxContents:
            self.listboxContents[item] = self.listboxContents[item] + 1
        else:
            self.listboxContents[item] = 1

    def RemoveItem(self, item):
        if item in self.listboxContents:
            if self.listboxContents[item] > 1: 
                self.listboxContents[item] = self.listboxContents[item] - 1
            else:
                self.listboxContents[item] = 0
        
    def SavePrices(self):
        a_file = open("prices.json", "w")
        json.dump(self.listBoxPrices, a_file)
        a_file.close()

    def LoadPrices(self):
        if(os.path.isfile('prices.json')):
            with open('prices.json') as json_file: 
                data = json.load(json_file)
                self.listBoxPrices = data
        #print(self.listBoxPrices)
            
    def UpdateListBoxGui(self):
        self.listbox.Clear()
        cats = self.OrderedCategories()
        for cat in cats:
            self.listbox.Append(""+cat+"" + ":")
            for item in sorted(cats[cat]):
                if(self.listboxContents[item] > 0):
                    itemName = "   " + item + "  "
                    if(self.listboxContents[item] > 1):
                        itemName = itemName +"x" + str(self.listboxContents[item])
                    
                    if(item in self.listBoxPrices):
                        itemName = itemName +  " | " + str(self.listBoxPrices[item])
                    self.listbox.Append(itemName)
            self.listbox.Append(" ")
        #print(self.listBoxPrices)

    def OrderedCategories(self):
        categories = {"Augment": "Augment", "Remove": "Remove(?!.*add).*$", "Remove\Add": "Remove.*add", "Change": "Change"}
        categoryContents = {"Augment": [], "Remove": [], "Remove\Add": [], "Change":[]}
        other = {"Other:": []}
        for cat in categories:
            for item in self.listboxContents:
                if(re.match(categories[cat],item)):
                   categoryContents[cat].append(item)

        for item in self.listboxContents:
            isOther=True
            for cat in categories:
                if item in categoryContents[cat]:
                    isOther=False
            if(isOther):
                other["Other:"].append(item)
                    
            
        #print(categoryContents)
        categoryContents.update(other)
        return categoryContents
                   
    def FixStupidNames(self, name):
        keeplist = [
            'Augment',
            'add',
            'Remove',
            'Life',
            'non-Life',
            'Defence',
            'non-Defence',
            'Lightning',
            'non-Lightning',
            'Enchant',
            'Map',
            'Tormented',
            'Spirits',
            'non-Cold',
            'Cold',
            'Fire',
            'non-Fire',
            'Chaos',
            'non-Chaos',
            'Green',
            'non-Green',
            'Blue',
            'non-Blue',
            'White',
            'non-White',
            'Red',
            'non-Red',
            'Reforge',
            'Caster',
            'non-Caster',
            'Attack',
            'non-Attack',
            'Physical',
            'non-Physical',
            'Critical',
            'non-Critical',
            'Prefix',
            'Prefix,',
            'Suffix',
            'Implicit',
            'Lucky',
            'Change',
            'Resistance'
            'Rare',
            #'Normal',
            #'Magic',
            'Reroll',
            'more',
            'common',
            #'values',
            'Sacrifice',
            'Fragments',
            'Corrupted',
            'Gem',
            '20%',
            '30%',
            '40%',
            '50%',
            'create',
            'Weapon',
            'Armor',
            'Jewel',
            'Facetor´s',
            'Prisms',
            'Unique',
            'Beachhead',
            'experience',
            'Set',
            'Implicit',
            'Cluster',
            'same',
            'tier',
            'half',
            'twice',
            '(75)',
            '(74)',
            '(73)',
            '(72)',
            '(71)',
            '(70)',
            '(69)',
            '(68)',
            '(67)',
            'Quality',
            '10%.',
            'Flask',
            
            ]
        parts = name.split(" ")
        #print(parts)
        temp = []
        for elem in parts: 
            if elem in keeplist: 
                temp.append(elem)
        #print(temp)
        if len(temp) < 2:
            parts.pop()
            return ' '.join(parts)
        return ' '.join(temp)

    def OnTogglePoll(self, event):
        self.pollActive = not self.pollActive
        if(self.pollActive):
            self.polBtn.SetBackgroundColour(wx.Colour(100, 0, 0))
        else:
            self.polBtn.SetBackgroundColour(wx.Colour(240, 240, 240))

        #print(self.pollActive)
        self.Poll()

        
    def Poll(self):
        if self.pollActive:
            t = threading.Timer(0.1, self.CheckClipboardContents)        
            t.start()

    def ClearClipboard(self):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(' ')
        win32clipboard.CloseClipboard()

    def SetClipBoardText(self, text):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()        
    

    def CheckClipboardContents(self):
        # get clipboard data
        #print("checked")
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        if "Horti" in data:
            self.Beep()
            self.ProcessClipboardContents(data)
            self.ClearClipboard()
        self.Poll()
            
    def Beep(self):
        duration = 100  # milliseconds
        freq = 240  # Hz
        winsound.Beep(freq, duration)

    def Boop(self):
        duration = 300  # milliseconds
        freq = 540  # Hz
        winsound.Beep(freq, duration)        

def main():

    app = wx.App()
    ex = HortiCraftLister(None, title='HortiCraftLister')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
