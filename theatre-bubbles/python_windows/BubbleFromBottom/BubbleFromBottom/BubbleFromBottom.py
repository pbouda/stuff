import sys
import wpf

from System import InvalidOperationException, DateTime, Uri, UriKind, TimeSpan
from System.Windows import Application, Window, Point, MessageBox, Thickness, FontWeights, Duration
from System.Windows.Controls import Image, Canvas, TextBox
from System.Windows.Media import Brush, SolidColorBrush, Color
from System.Windows.Media.Animation import DoubleAnimation, Storyboard
from System.Windows.Media.Imaging import BitmapImage, BitmapCacheOption

class MainWindow(Window):
    def __init__(self):
        self.gui = wpf.LoadComponent(self, 'BubbleFromBottom.xaml')
        #self.create_runtime()

        self.Loaded += self.on_loaded
        #self.Closing += self.on_closing

        self.thinkBubble = BitmapImage()
        self.thinkBubble.BeginInit()
        self.thinkBubble.UriSource = Uri("think2.png", UriKind.Relative);
        self.thinkBubble.CacheOption = BitmapCacheOption.OnLoad;
        #self.thinkBubble.Height = 150
        #self.thinkBubble.Width = 150
        self.thinkBubble.EndInit();

        self.currentX = 300.0
        self.currentY = 700.0

    def on_loaded(self, s, e):
        bubble = Image()
        bubble.Name = "Bubble"
        #imageSource = System.Windows.Resources["think"]
        bubble.Source = self.thinkBubble
        bubble.SetValue(Canvas.TopProperty, self.currentY)
        bubble.SetValue(Canvas.LeftProperty, self.currentX)
        self.mainPanel.Children.Add(bubble)

        text = TextBox()
        text.Text = "Hello World!"
        text.FontSize = 50
        text.FontWeight = FontWeights.Bold
        text.BorderThickness = Thickness(0)
        text.SetValue(Canvas.TopProperty, self.currentY + 120)
        text.SetValue(Canvas.LeftProperty, self.currentX + 60)
        self.mainPanel.Children.Add(text)

        myDoubleAnimation = DoubleAnimation()
        myDoubleAnimation.From = 770.0;
        myDoubleAnimation.To = 300.0;

        myDoubleAnimation.Duration = Duration(TimeSpan.FromSeconds(3))

        myDoubleAnimationText = DoubleAnimation()
        myDoubleAnimationText.From = 770.0 + 120.0;
        myDoubleAnimationText.To = 300.0 + 120.0;

        myDoubleAnimationText.Duration = Duration(TimeSpan.FromSeconds(3))

        #myStoryboard = Storyboard()
        #myStoryboard.Children.Add(myDoubleAnimation)
        #Storyboard.SetTargetName(myDoubleAnimation, bubble.Name)
        #Storyboard.SetTargetProperty(myDoubleAnimation, PropertyPath(Canvas.TopProperty))

        #myStoryboard.Begin(self);

        bubble.BeginAnimation(Canvas.TopProperty, myDoubleAnimation)
        text.BeginAnimation(Canvas.TopProperty, myDoubleAnimationText)

if __name__ == '__main__':
    Application().Run(MainWindow())
