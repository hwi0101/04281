# -*- coding: big5
# 若程式中有使用中文，必須指明使用BIG5碼，前述的字碼定義必須在程式的第一或第二行
# 字碼定義的方式可參考：http://www.python.org/dev/peps/pep-0263/
# Python支援的字碼： http://www.python.org/doc/2.4/lib/standard-encodings.html

""" 此程式示作為檢查航照影像是否涵蓋機敏區的程式之GUI介面 """

import os, sys
import wx
from math import sin, cos, tan, radians

from latlon2twd import LatLonToTWD97
from twd2latlon import TMToLatLon
from math import degrees,radians

# some global variables
currDir = os.getcwd()
transformType = 1    # default transformation type (1: TWD97 to WGS84)

#---------------------------------------------------------------------------

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        #建造一個新的 Frame
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title="坐標轉換工具", size=(540,320),
                style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)

        # 設定 Icon 影像
        ico = wx.Icon('AFASILogo.bmp', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
                
        # 加入一個 Panel
        panel = wx.Panel(self, wx.ID_ANY)
        
        # 輸入坐標
        wx.StaticText(parent=panel, label="輸入坐標(x,y) or (lat,lon):", pos=(15,10))
        self.a = wx.TextCtrl(parent=panel,pos=(200,10),size=(265,20))

        # 坐標轉換模式選項
        label_1 = ['TWD97 to WGS84', 'WGS to TWD97']
        self.rbox1 = wx.RadioBox(parent=panel, label = '', pos = (180,40), choices = label_1,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.OnType)

        # 清除訊息按鈕
        self.btn1 = wx.Button(parent=panel,label=" 清除訊息 ",pos=(15,55),size=(100,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn1, self.btn1)

        # 確定按鈕
        self.btn2 = wx.Button(parent=panel,label=" 確定 ",pos=(460,55),size=(60,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn2, self.btn2)

        self.txtCtrl = wx.TextCtrl(panel, id=wx.ID_ANY, style=wx.TE_MULTILINE, pos=(10,90), size=(510,180))


    # 設定坐標轉換模式
    def OnType(self, event):
        global transformType
        
        selType = self.rbox1.GetStringSelection()
        
        if selType == 'TWD97 to WGS84':
            transformType = 1
        else:
            transformType = 2

        self.txtCtrl.WriteText('\n坐標轉換類型： %s\n' % selType)
    
    # 清除訊息
    def OnBtn1(self, evt):
        
        self.txtCtrl.Clear()

    # 確定按鈕，開始執行
    def OnBtn2(self, evt):
        
        try:
            # 取得輸入坐標
            in_str = self.a.GetValue()
            self.txtCtrl.WriteText('輸入坐標資料： %s\n' % in_str)
            
            s1, s2 = in_str.split(',')
            v1 = float(s1)
            v2 = float(s2)
            
            # 檢查轉換模式
            if transformType == 1:
                # TWD97 轉換為 WGS84
                c = TMToLatLon()
                lat, lon = c.convert(v1, v2)
                self.txtCtrl.WriteText('\n緯度, 經度： {}, {}\n'.format(lat, lon))
            else:
                # WGS84 轉換為 TWD97
                c = LatLonToTWD97()
                lat = radians(float(v1))
                lon = radians(float(v2))
                x, y = c.convert(lat, lon)
                self.txtCtrl.WriteText('\nX, Y： {}, {}\n'.format(x, y))
                
            self.txtCtrl.WriteText('成功!\n')
        except:
            self.txtCtrl.WriteText('失敗!\n')
        
#---------------------------------------------------------------------------

# Every wxWidgets application must have a class derived from wx.App
class MyApp(wx.App):

    # wxWindows calls this method to initialize the application
    def OnInit(self):

        # Create an instance of our customized Frame class
        frame = MyFrame(None, -1, "Coordinate Transformation")
        frame.Show(True)

        # Tell wxWindows that this is our main window
        self.SetTopWindow(frame)

        # Return a success flag
        return True
        
#---------------------------------------------------------------------------
    
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()

