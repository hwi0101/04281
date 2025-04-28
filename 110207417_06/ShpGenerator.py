# -*- coding: utf-8 -*-
import os
import wx
import shapefile
import shutil

# 全域參數
inDir = ""
currDir = os.getcwd()
outFile = ""

#---------------------------------------------------------------------------

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        # New Frame
        wx.Frame.__init__(self, parent=None, title="Shapefile Generator", size=(540,550),
                style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        
        # Icon
        ico = wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        
        # New Panel
        panel = wx.Panel(self, wx.ID_ANY)
        
        # 功能
        wx.StaticText(parent=panel, label="請輸入sel檔案", pos=(15,10))
        self.a = wx.TextCtrl(parent=panel,pos=(140,10),size=(325,20))
        self.btn1 = wx.Button(parent=panel,label="...",pos=(480,10),size=(40,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn1, self.btn1)
        
        wx.StaticText(parent=panel, label="輸出shapefile資料檔", pos=(15,40))
        self.b = wx.TextCtrl(parent=panel,pos=(140,40),size=(325,20))
        self.btn2 = wx.Button(parent=panel,label="...",pos=(480,40),size=(40,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn2, self.btn2)
        
        self.btn3 = wx.Button(parent=panel, label="清除訊息", pos=(15,70), size=(100,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn3, self.btn3)
        
        self.btn4 = wx.Button(parent=panel,label=" 確定 ",pos=(460,70),size=(60,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn4, self.btn4)
        
        # 訊息欄
        self.txtCtrl = wx.TextCtrl(panel, id=wx.ID_ANY, style=wx.TE_MULTILINE, pos=(10,110), size=(510,390))
    
    def OnBtn1(self, evt):
        global inDir
        # 對話框
        dlg = wx.FileDialog(self, message="請輸入sel檔案")
        
        # 用戶點選OK後執行
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.a.SetValue(path)
            inDir = self.a.GetValue()
            inDir = inDir.replace('\\', '/')
        
        # 關閉對話框
        dlg.Destroy()
        
    def OnBtn2(self, evt):
        global outFile
        
        # 選擇要輸出到哪個資料夾
        dlg = wx.FileDialog(self, message="選擇輸出資料夾", defaultDir=currDir, defaultFile="", 
                            wildcard="*.shp",
                            style= wx.FD_OVERWRITE_PROMPT | wx.FD_SAVE
                            )
        
        # 用戶點選Save後執行
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.b.SetValue(path)
            outFile = self.b.GetValue()
            outFile = outFile.replace('\\', '/')
        
        dlg.Destroy()
        
    def OnBtn3(self, evt):
        self.txtCtrl.Clear()
    
    def OnBtn4(self, evt):
        #執行函式
        try:
            self.txtCtrl.WriteText('輸入檔案： %s\n' % inDir)
            self.shp_generate()

            self.txtCtrl.WriteText('輸出檔案： %s\n' % outFile)
            self.txtCtrl.WriteText('成功\n')
        except:
            print('失敗!~')
            self.txtCtrl.WriteText("失敗\n")
            
    def shp_generate(self):
        global outFile
        try:
            fin = open(inDir[-7:], encoding = "big5")
            print("讀取檔案中...")
        except:
            print("失敗！")
            self.txtCtrl.WriteText("失敗2\n")
        
        shp = shapefile.Writer(outFile, shapeType = shapefile.POINT)
        
        shp.field('NAME','C',16)
        shp.field('E97','N',15,3)
        shp.field('N97','N',15,3)
        shp.field('H97','N',4,3)
        shp.field('E67','N',15,3)
        shp.field('N67','N',15,3)
        shp.field('H67','N',4,3)
        shp.field('LN','C',2)
        shp.field('DATE','C',8)
        shp.field('TIME','C',4)
        shp.field('SEC','N',2,3)

        count = 0
        for line in fin:
           count = count + 1
           if count <= 2:
               continue
           NAME = line[:10] + "_" + line[11:16]
           E97 = float(line[17:27])
           N97 = float(line[28:39])
           H97 = float(line[40:48])
           E67 = float(line[50:60])
           N67 = float(line[61:72])
           H67 = float(line[73:81])
           LN = line[82:84]
           DATE = line[85:93]
           TIME = line[94:98]
           SEC = float(line[99:105])
           
           shp.point(float(line[17:27]),float(line[28:39]))
           shp.record(NAME,E97,N97,H97,E67,N67,H67,LN,DATE,TIME,SEC)
           
        
        
        try:
            shp.close()
            prj_file = 'TM2.prj'
            prj_out = outFile[:-3] + 'prj'
            shutil.copyfile(prj_file, prj_out)
            self.txtCtrl.WriteText("成功")
        except:
            self.txtCtrl.WriteText("失敗3\n")
         
        fin.close()

           
#-----------------------------------------            
         
class MyApp(wx.App):

    # 初始化
    def OnInit(self):
        frame = MyFrame(None, -1, "Create Worldfile")
        frame.Show(True)

        self.SetTopWindow(frame)

        return True

#-----------------------------------------

if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        