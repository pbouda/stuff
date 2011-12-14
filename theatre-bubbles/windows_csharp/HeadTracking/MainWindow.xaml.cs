/////////////////////////////////////////////////////////////////////////
//
// This module contains code to do Kinect NUI initialization and
// processing and also to display NUI streams on screen.
//
// Copyright © Microsoft Corporation.  All rights reserved.  
// This code is licensed under the terms of the 
// Microsoft Kinect for Windows SDK (Beta) from Microsoft Research 
// License Agreement: http://research.microsoft.com/KinectSDK-ToU
//
/////////////////////////////////////////////////////////////////////////
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Microsoft.Research.Kinect.Nui;

namespace SkeletalViewer
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        Runtime nui;
        DateTime lastTime = DateTime.MaxValue;
        Point lastPos = new Point(0, 0);
        
        private void Window_Loaded(object sender, EventArgs e)
        {
            nui = new Runtime();

            try
            {
                nui.Initialize(RuntimeOptions.UseDepthAndPlayerIndex | RuntimeOptions.UseSkeletalTracking | RuntimeOptions.UseColor);
            }
            catch (InvalidOperationException)
            {
                System.Windows.MessageBox.Show("Runtime initialization failed. Please make sure Kinect device is plugged in.");
                return;
            }

            lastTime = DateTime.Now;

            nui.SkeletonFrameReady += new EventHandler<SkeletonFrameReadyEventArgs>(nui_SkeletonFrameReady);
        }


        private Point getDisplayPosition(Joint joint)
        {
            float depthX, depthY;
            nui.SkeletonEngine.SkeletonToDepthImage(joint.Position, out depthX, out depthY);
            depthX = depthX * 320; //convert to 320, 240 space
            depthY = depthY * 240; //convert to 320, 240 space
            int colorX, colorY;
            ImageViewArea iv = new ImageViewArea();
            // only ImageResolution.Resolution640x480 is supported at this point
            nui.NuiCamera.GetColorPixelCoordinatesFromDepthPixel(ImageResolution.Resolution640x480, iv, (int)depthX, (int)depthY, (short)0, out colorX, out colorY);

            // map back to skeleton.Width & skeleton.Height
            return new Point((int)(skeleton.Width * colorX / 640.0), (int)(skeleton.Height * colorY / 480));
        }


        void nui_SkeletonFrameReady(object sender, SkeletonFrameReadyEventArgs e)
        {
            SkeletonFrame skeletonFrame = e.SkeletonFrame;
            int iSkeleton = 0;

            skeleton.Children.Clear();
            foreach (SkeletonData data in skeletonFrame.Skeletons)
            {
                if (SkeletonTrackingState.Tracked == data.TrackingState)
                {

                    // Draw joints
                    Boolean foundHead = false;
                    foreach (Joint joint in data.Joints)
                    {
                        if (joint.ID == JointID.Head)
                        {
                            Point jointPos = getDisplayPosition(joint);
                            Image bubble = new Image();
                            ImageSource imageSource = (ImageSource)FindResource("think"); 
                            bubble.Source = imageSource;
                            bubble.SetValue(Canvas.TopProperty, 200.0);
                            bubble.SetValue(Canvas.LeftProperty, 1280 - jointPos.X);
                            skeleton.Children.Add(bubble);
                            lastPos = jointPos;
                            foundHead = true;
                        }
                    }
                    if (!foundHead)
                    {
                        Image bubble = new Image();
                        ImageSource imageSource = (ImageSource)FindResource("think");
                        bubble.Source = imageSource;
                        bubble.SetValue(Canvas.TopProperty, 200.0);
                        bubble.SetValue(Canvas.LeftProperty, 1280 - lastPos.X);
                        skeleton.Children.Add(bubble);
                    }
                }
                iSkeleton++;
            } // for each skeleton
        }

        private void Window_Closed(object sender, EventArgs e)
        {
            nui.Uninitialize();
            Environment.Exit(0);
        }

    }
}
