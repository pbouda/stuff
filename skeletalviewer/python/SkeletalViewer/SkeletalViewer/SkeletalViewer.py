import sys
import wpf
import clr
clr.AddReferenceToFile("Microsoft.Research.Kinect.dll")

from System import InvalidOperationException, DateTime, Uri, UriKind
from System.Windows import Application, Window, Point, MessageBox
from System.Windows.Controls import Image, Canvas
from System.Windows.Media import Brush, SolidColorBrush, Color
from System.Windows.Media.Imaging import BitmapImage, BitmapCacheOption
from Microsoft.Research.Kinect.Nui import Runtime, RuntimeOptions, \
    JointID, ImageStreamType, ImageResolution, JointID, SkeletonTrackingState, \
    ImageViewArea

class MainWindow(Window):
    def __init__(self):
        self.gui = wpf.LoadComponent(self, 'SkeletalViewer.xaml')
        #self.create_runtime()

        self.Loaded += self.on_loaded
        self.Closing += self.on_closing

        self.thinkBubble = BitmapImage()
        self.thinkBubble.BeginInit()
        self.thinkBubble.UriSource = Uri("think.png", UriKind.Relative);
        self.thinkBubble.CacheOption = BitmapCacheOption.OnLoad;
        self.thinkBubble.EndInit();

    def on_loaded(self, s, e):
        self.nui = Runtime()

        if not self.nui:
            MessageBox.Show("Runtime initialization failed. Please make sure Kinect device is plugged in.")
            return

        self.nui.Initialize(RuntimeOptions.UseSkeletalTracking)
        self.nui.SkeletonFrameReady += self.nui_skeleton_frame_ready

    def getDisplayPosition(self, joint):
        depthX, depthY = self.nui.SkeletonEngine.SkeletonToDepthImage(joint.Position)
        depthX = depthX * 320
        depthY = depthY * 240
        iv = ImageViewArea()

        # only ImageResolution.Resolution640x480 is supported at this point
        colorX, colorY = self.nui.NuiCamera.GetColorPixelCoordinatesFromDepthPixel(ImageResolution.Resolution640x480, iv, depthX, depthY, 0)

        # map back to skeleton.Width & skeleton.Height
        return Point( (self.skeleton.Width * colorX / 640.0), (self.skeleton.Height * colorY / 480) )

    def nui_skeleton_frame_ready(self, sender, e):
        skeletonFrame = e.SkeletonFrame
        self.skeleton.Children.Clear()

        for data in skeletonFrame.Skeletons:
            if SkeletonTrackingState.Tracked == data.TrackingState:
                foundHead = False
                for joint in data.Joints:
                    if joint.ID == JointID.Head:
                        jointPos = self.getDisplayPosition(joint)
                        bubble = Image()
                        #imageSource = System.Windows.Resources["think"]
                        bubble.Source = self.thinkBubble
                        bubble.SetValue(Canvas.TopProperty, 200.0)
                        bubble.SetValue(Canvas.LeftProperty, 1280 - jointPos.X)
                        self.skeleton.Children.Add(bubble)
                        lastPos = jointPos
                        foundHead = True




    def on_closing(self, s, e):
        self.nui.Uninitialize();

if __name__ == '__main__':
    Application().Run(MainWindow())
