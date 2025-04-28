# -*- coding: big5
# �Y�{�������ϥΤ���A���������ϥ�BIG5�X�A�e�z���r�X�w�q�����b�{�����Ĥ@�βĤG��
# �r�X�w�q���覡�i�ѦҡGhttp://www.python.org/dev/peps/pep-0263/
# Python�䴩���r�X�G http://www.python.org/doc/2.4/lib/standard-encodings.html

""" ���{���ܧ@���ˬd��Ӽv���O�_�[�\���ӰϪ��{����GUI���� """

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
        #�سy�@�ӷs�� Frame
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title="�����ഫ�u��", size=(540,320),
                style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)

        # �]�w Icon �v��
        ico = wx.Icon('AFASILogo.bmp', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
                
        # �[�J�@�� Panel
        panel = wx.Panel(self, wx.ID_ANY)
        
        # ��J����
        wx.StaticText(parent=panel, label="��J����(x,y) or (lat,lon):", pos=(15,10))
        self.a = wx.TextCtrl(parent=panel,pos=(200,10),size=(265,20))

        # �����ഫ�Ҧ��ﶵ
        label_1 = ['TWD97 to WGS84', 'WGS to TWD97']
        self.rbox1 = wx.RadioBox(parent=panel, label = '', pos = (180,40), choices = label_1,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        self.rbox1.Bind(wx.EVT_RADIOBOX, self.OnType)

        # �M���T�����s
        self.btn1 = wx.Button(parent=panel,label=" �M���T�� ",pos=(15,55),size=(100,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn1, self.btn1)

        # �T�w���s
        self.btn2 = wx.Button(parent=panel,label=" �T�w ",pos=(460,55),size=(60,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn2, self.btn2)

        self.txtCtrl = wx.TextCtrl(panel, id=wx.ID_ANY, style=wx.TE_MULTILINE, pos=(10,90), size=(510,180))


    # �]�w�����ഫ�Ҧ�
    def OnType(self, event):
        global transformType
        
        selType = self.rbox1.GetStringSelection()
        
        if selType == 'TWD97 to WGS84':
            transformType = 1
        else:
            transformType = 2

        self.txtCtrl.WriteText('\n�����ഫ�����G %s\n' % selType)
    
    # �M���T��
    def OnBtn1(self, evt):
        
        self.txtCtrl.Clear()

    # �T�w���s�A�}�l����
    def OnBtn2(self, evt):
        
        try:
            # ���o��J����
            in_str = self.a.GetValue()
            self.txtCtrl.WriteText('��J���и�ơG %s\n' % in_str)
            
            s1, s2 = in_str.split(',')
            v1 = float(s1)
            v2 = float(s2)
            
            # �ˬd�ഫ�Ҧ�
            if transformType == 1:
                # TWD97 �ഫ�� WGS84
                c = TMToLatLon()
                lat, lon = c.convert(v1, v2)
                self.txtCtrl.WriteText('\n�n��, �g�סG {}, {}\n'.format(lat, lon))
            else:
                # WGS84 �ഫ�� TWD97
                c = LatLonToTWD97()
                lat = radians(float(v1))
                lon = radians(float(v2))
                x, y = c.convert(lat, lon)
                self.txtCtrl.WriteText('\nX, Y�G {}, {}\n'.format(x, y))
                
            self.txtCtrl.WriteText('���\!\n')
        except:
            self.txtCtrl.WriteText('����!\n')
        
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

