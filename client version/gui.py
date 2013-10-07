#!---coding=utf-8---
import wx

class ChoiceFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Ç©µ½',size=(400,350),style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        panel = wx.Panel(self, -1)
        sampleList = ['Chrome','FireFox','IE','360']
        wx.StaticText(panel, -1, "Choose:", (40, 20))
        wx.Choice(panel, -1, (100, 18), choices=sampleList)
	self.button = wx.Button(panel, -1, "Ç©µ½", pos=(245, 16))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
	self.output=wx.TextCtrl(panel,-1,pos=(40,60),size=(300,200),style=wx.TE_READONLY|wx.TE_MULTILINE)
    def OnClick(self, event):
	pass

if __name__ == '__main__':
    app = wx.App()
    ChoiceFrame().Show()
    app.MainLoop() 
