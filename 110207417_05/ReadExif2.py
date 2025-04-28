# -*- coding: big5
# �Y�{�������ϥΤ���A���������ϥ�BIG5�X�A�e�z���r�X�w�q�����b�{�����Ĥ@�βĤG��
# �r�X�w�q���覡�i�ѦҡGhttp://www.python.org/dev/peps/pep-0263/
# Python�䴩���r�X�G http://www.python.org/doc/2.4/lib/standard-encodings.html

""" ���{���ܧ@���ˬd��Ӽv���O�_�[�\���ӰϪ��{����GUI���� """

import os, sys
import wx
import exifread

import glob
#import datetime
#import numpy as np
#from skimage import io
#from skimage.transform import resize

# some global variables
inDir = ""
currDir = os.getcwd()
outFile = ""

#---------------------------------------------------------------------------

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        #�سy�@�ӷs�� Frame
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title="EXIF Reader", size=(540,550),
                style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)

        #logo_path = resource_path("nccu_logo.bmp")
        #self.window.iconbitmap(image_path)
        ico = wx.Icon("nccu_logo.bmp", wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
                
        # �[�J�@�� Panel
        panel = wx.Panel(self, wx.ID_ANY)
        
        wx.StaticText(parent=panel, label="��J��Ƨ�:", pos=(15,10))
        self.a = wx.TextCtrl(parent=panel,pos=(140,10),size=(325,20))
        self.btn1 = wx.Button(parent=panel,label="...",pos=(480,10),size=(40,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn1, self.btn1)

        wx.StaticText(parent=panel, label="��X�����:", pos=(15,40))
        self.b = wx.TextCtrl(parent=panel,pos=(140,40),size=(325,20))
        self.btn2 = wx.Button(parent=panel,label="...",pos=(480,40),size=(40,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn2, self.btn2)

        self.btn3 = wx.Button(parent=panel,label=" �M���T�� ",pos=(15,70),size=(100,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn3, self.btn3)

        self.btn4 = wx.Button(parent=panel,label=" �T�w ",pos=(460,70),size=(60,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn4, self.btn4)

        self.txtCtrl = wx.TextCtrl(panel, id=wx.ID_ANY, style=wx.TE_MULTILINE, pos=(10,110), size=(510,390))

        #self.readConfigFile()
#            self.writeConfigFile()

    def OnBtn1(self, evt):
        global inDir
        # In this case we include a "New directory" button. 
        dlg = wx.DirDialog(
            self, message="��ܿ�J��Ƨ�:",
            style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
            )
                     
        # If the user selects OK, then we process the dialog's data.
        # This is done by getting the path data from the dialog - BEFORE
        # we destroy it. 
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            path = dlg.GetPath()
            self.a.SetValue(path)
            inDir = self.a.GetValue()
            inDir = inDir.replace('\\', '/')
            
        # Only destroy a dialog after you're done with it.
        dlg.Destroy()

    def OnBtn2(self, evt):
        global outFile
        
        # Choose the output file. 
        dlg = wx.FileDialog(
            self, message="��ܿ�X�����:",
            defaultDir=currDir, 
            defaultFile="",
            wildcard="*.csv",
            style= wx.FD_OVERWRITE_PROMPT | wx.FD_SAVE
            )
                     
        # If the user selects OK, then we process the dialog's data.
        # This is done by getting the path data from the dialog - BEFORE
        # we destroy it. 
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            path = dlg.GetPath()
            self.b.SetValue(path)
            outFile = self.b.GetValue()
            outFile = outFile.replace('\\', '/')
            
        # Only destroy a dialog after you're done with it.
        dlg.Destroy()

    def OnBtn3(self, evt):
        
        self.txtCtrl.Clear()

    def OnBtn4(self, evt):
        
        try:
            self.txtCtrl.WriteText('��J��Ƨ��G %s\n' % inDir)
            self.read_exif()
            self.txtCtrl.WriteText('��X�ɮסG %s\n' % outFile)
            self.txtCtrl.WriteText('���\!\n')
        except:
            print('����!')
        
    def read_exif(self):
        
        img_list = glob.glob("%s/*.jpg" % inDir)
        
        num_img = len(img_list)
        
        if num_img == 0:
            self.txtCtrl.WriteText('�䤣�� JPG �v����!\n')
            return
        
        fout = open(outFile, 'w')
        header = '�ɮצW��,����ɶ�,�g��,�n��\n'
        fout.write(header)

        for i in range(num_img):
            basename = os.path.basename(img_list[i])
            #print(basename)
            
            img = exifread.process_file(open(img_list[i],'rb'))
            time = img['Image DateTime']
            
            try:
                lat_str = str(img['GPS GPSLatitude'])
                lat = format_lat_lon(lat_str)
                lon_str = str(img['GPS GPSLongitude'])
                lon = format_lat_lon(lon_str)
                
                data = '{},{},{},{}\n'.format(basename, time, lon, lat)
            except:
                self.txtCtrl.WriteText('%s has no GPS info\n' % basename)
                data = '{},{}\n'.format(basename, time)
                
            self.txtCtrl.WriteText(data)
            
            fout.write(data)
            
        fout.close()
#---------------------------------------------------------------------------

def format_lat_lon(data):
    t = data.replace('[', '').replace(']', '').split(',')
    dd = float(t[0].strip())
    mm = float(t[1].strip()) / 60
    s = t[2].strip().split('/')
    ss = float(s[0]) / float(s[1]) / 3600
    
    result = dd + mm + ss
    return result

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    
#---------------------------------------------------------------------------

# Every wxWidgets application must have a class derived from wx.App
class MyApp(wx.App):

    # wxWindows calls this method to initialize the application
    def OnInit(self):

        # Create an instance of our customized Frame class
        frame = MyFrame(None, -1, "Create Worldfile")
        frame.Show(True)

        # Tell wxWindows that this is our main window
        self.SetTopWindow(frame)

        # Return a success flag
        return True
        
#---------------------------------------------------------------------------
    
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()

