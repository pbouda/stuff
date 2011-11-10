import sys
import wpf
import clr
clr.AddReferenceToFile("Microsoft.Research.Kinect.dll")

from System import InvalidOperationException, DateTime
from System.Windows import Application, Window, Point, MessageBox
from System.Windows.Media import Brush, SolidColorBrush, Color
from Microsoft.Research.Kinect.Nui import Runtime, RuntimeOptions, \
    JointID, ImageStreamType, ImageResolution, ImageType

RED_IDX = 2
GREEN_IDX = 1
BLUE_IDX = 0

class MainWindow(Window):
    def __init__(self):
        self.gui = wpf.LoadComponent(self, 'SkeletalViewer.xaml')
        #self.create_runtime()
        self.last_time = DateTime.MaxValue
        self.totalFrames = 0
        self.lastFrames = 0
        self.depthFrame32 = list()

        self.Loaded += self.on_loaded
        self.Closing += self.on_closing

    def on_loaded(self, s, e):
        self.nui = Runtime()
        try:
            self.nui.Initialize(RuntimeOptions.UseDepthAndPlayerIndex | RuntimeOptions.UseSkeletalTracking | RuntimeOptions.UseColor)
        except(InvalidOperationException):
            MessageBox.Show("Runtime initialization failed. Please make sure Kinect device is plugged in.")
            return

        try:
            self.nui.VideoStream.Open(ImageStreamType.Video, 2, ImageResolution.Resolution640x480, ImageType.Color)
            self.nui.DepthStream.Open(ImageStreamType.Depth, 2, ImageResolution.Resolution320x240, ImageType.DepthAndPlayerIndex)
        except(InvalidOperationException):
            MessageBox.Show("Failed to open stream. Please make sure to specify a supported image type and resolution.");
            return

        self.last_time = DateTime.Now
        #self.nui.DepthFrameReady += self.nui_DepthFrameReady
        self.nui.SkeletonFrameReady += self.nui_skeleton_frame_ready
        #self.nui.VideoFrameReady += self.nui_ColorFrameReady

    def nui_skeleton_frame_ready(self, sender, e):
        skeletonFrame = e.SkeletonFrame
        iSkeleton = 0
        brushes = list()
        brushes.append(SolidColorBrush(Color.FromRgb(255, 0, 0)))
        brushes.append(SolidColorBrush(Color.FromRgb(0, 255, 0)))
        brushes.append(SolidColorBrush(Color.FromRgb(64, 255, 255)))
        brushes.append(SolidColorBrush(Color.FromRgb(255, 255, 64)))
        brushes.append(SolidColorBrush(Color.FromRgb(255, 64, 255)))
        brushes.append(SolidColorBrush(Color.FromRgb(128, 128, 255)))

        self.skeleton.Children.Clear()

    def on_closing(self, s, e):
        self.nui.Uninitialize();

if __name__ == '__main__':
    Application().Run(MainWindow())
