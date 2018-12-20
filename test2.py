import wx


class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(350, 250))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        l1 = wx.StaticText(panel, -1, "文本域")

        hbox1.Add(l1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.t1 = wx.TextCtrl(panel)

        hbox1.Add(self.t1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.t1.Bind(wx.EVT_TEXT, self.OnKeyTyped)
        vbox.Add(hbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        l2 = wx.StaticText(panel, -1, "密码文本")

        hbox2.Add(l2, 1, wx.ALIGN_LEFT | wx.ALL, 5)
        self.t2 = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        self.t2.SetMaxLength(5)

        hbox2.Add(self.t2, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(hbox2)
        self.t2.Bind(wx.EVT_TEXT_MAXLEN, self.OnMaxLen)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        l3 = wx.StaticText(panel, -1, "多行文本")

        hbox3.Add(l3, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.t3 = wx.TextCtrl(panel, size=(200, 100), style=wx.TE_MULTILINE)

        hbox3.Add(self.t3, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(hbox3)
        self.t3.Bind(wx.EVT_TEXT_ENTER, self.OnEnterPressed)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        l4 = wx.StaticText(panel, -1, "只读取文本")

        hbox4.Add(l4, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.t4 = wx.TextCtrl(panel, value="只读文本", style=wx.TE_READONLY | wx.TE_CENTER)

        hbox4.Add(self.t4, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(hbox4)
        panel.SetSizer(vbox)

        self.Centre()
        self.Show()
        self.Fit()

    def OnKeyTyped(self, event):
        print(event.GetString())

    def OnEnterPressed(self, event):
        print("Enter pressed")

    def OnMaxLen(self, event):
        print("Maximum length reached")


app = wx.App()
Mywin(None, 'TextCtrl实例-www.yiibai.com')
app.MainLoop()