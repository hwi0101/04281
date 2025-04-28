import wx
from twd2latlon import TMToLatLon

class CoordinateConversionApp(wx.App):
    def OnInit(self):
        frame = CoordinateConversionFrame(None, title=" GUI ")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

class CoordinateConversionFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(CoordinateConversionFrame, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        button = wx.Button(panel, label="執行座標轉換")
        button.Bind(wx.EVT_BUTTON, self.on_convert)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button, flag=wx.ALL | wx.ALIGN_CENTER, border=10)
        panel.SetSizer(sizer)
        sizer.Fit(self)

    def on_convert(self, event):
        fin = open('108.sel')
        f = open("110207417.kml", "w", encoding="utf-8")

        c1 = TMToLatLon()

        head = """<?xml version="1.0" encoding="UTF-8"?>
            <kml xmlns="http://www.opengis.net/kml/2.2">
              <Document>
              <name>output.kml</name>
              <Style id="DownArrow">
                 <IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/pal4/icon28.png</href>
                            </Icon><scale>0.6</scale></IconStyle></Style>
              <Style id="UpArrow">
                 <IconStyle><Icon><href>https://earth.google.com/images/kml-icons/track-directional/track-0.png</href>
                            </Icon><scale>0.6</scale></IconStyle></Style>
               <Folder>
                 <name>Placemarks</name>
                 <description>output.kml</description>
        """
        f.write(head)

        mark1 = """
             <Placemark>
               <name>{}</name>
               <description>({}, {}, {})</description>
               <styleUrl>#DownArrow</styleUrl>
               <Point><altitudeMode>absolute</altitudeMode>
                      <coordinates>{},{},{}</coordinates></Point>
             </Placemark>  """

        count = 0
        for line in fin:
            count += 1
            if count <= 2:
                continue

            e_97 = float(line[17:27])
            n_97 = float(line[28:39])

            lat, lon = c1.convert(e_97, n_97)

            s = line.strip()
            t = s.split()

            t2 = float(line[17:27])
            t3 = float(line[28:39])
            t4 = float(line[40:48])
            t2_int = int(t2)
            t3_int = int(t3)
            t4_int = int(t4)
            if count == 28:
                break

            xml = mark1.format(t[0] + t[1], t2_int, t3_int, t4_int, lon, lat, t4)
            f.write(xml)
            f.write("\n")

        mark2 = """
             <Placemark>
               <name>{}</name>
               <description>({}, {}, {})</description>
               <styleUrl>#UpArrow</styleUrl>
               <Point><altitudeMode>absolute</altitudeMode>
                      <coordinates>{},{},{}</coordinates></Point>
             </Placemark>  """

        for line in fin:
            count += 1
            if count <= 28:
                continue

            e_97 = float(line[17:27])
            n_97 = float(line[28:39])

            lat, lon = c1.convert(e_97, n_97)

            s = line.strip()
            t = s.split()

            t2 = float(line[17:27])
            t3 = float(line[28:39])
            t4 = float(line[40:48])
            t2_int = int(t2)
            t3_int = int(t3)
            t4_int = int(t4)

            xml = mark2.format(t[0] + t[1], t2_int, t3_int, t4_int, lon, lat, t4)
            f.write(xml)
            f.write("\n")

        end = """ </Folder>
              </Document>
            </kml>
             """
        f.write(end)
        f.close()
        fin.close()

if __name__ == "__main__":
    app = CoordinateConversionApp(False)
    app.MainLoop()