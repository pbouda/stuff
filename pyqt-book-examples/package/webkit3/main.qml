import Qt 4.7
import QtWebKit 1.0
 
Rectangle {
    id: mainScreen
    
    width: 640
    height: 480

    color: "black"

    Item {
        id: codeView
        anchors.fill: parent

        Rectangle {        
            width: parent.width
    
            Text {
                anchors.left: parent.left
                horizontalAlignment: TextEdit.AlignLeft
                color: "white"
                text: mainScreen.width + " x " + mainScreen.height
            }
            Text {
                anchors.right: parent.right
                anchors.rightMargin: 20
                horizontalAlignment: TextEdit.AlignRight
                color: "blue"
                text: "<a href=\"https://github.com/pbouda/Process-\">Über</a>"
                onLinkActivated: Qt.openUrlExternally(link)
            }
        }

        Rectangle {
            id: codeViewGroup
            anchors.fill: parent
            anchors.margins: 20
            focus: true
            color: "lightgrey"
            border.color: "darkgrey"
            border.width: 5
            radius: 10
            
            Item {
                anchors.fill: parent
                anchors.horizontalCenter: parent.horizontalCenter
                width: parent.width
            
                Rectangle {
                    id: code
                    anchors.fill: parent
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.topMargin: 20
                    anchors.leftMargin: 10
                    anchors.rightMargin: 10
                    anchors.bottomMargin: 80
                    border.color: "grey"
                    border.width: 2
                    
                    Flickable {
                        id: flick
                   
                        width: parent.width; height: parent.height;
                        contentWidth: codeEditor.paintedWidth
                        contentHeight: codeEditor.paintedHeight
                        clip: true
                   
                        function ensureVisible(r)
                        {
                            if (contentX >= r.x)
                                contentX = r.x;
                            else if (contentX+width <= r.x+r.width)
                                contentX = r.x+r.width-width;
                            if (contentY >= r.y)
                                contentY = r.y;
                            else if (contentY+height <= r.y+r.height)
                                contentY = r.y+r.height-height;
                        }
        
                        TextEdit {
                            id: codeEditor
                            focus: true
                            width: flick.width
                            height: flick.height
                            wrapMode: TextEdit.Wrap
                            font.pixelSize: 24
                            font.family: "Lucida Console"
                            textFormat: TextEdit.PlainText
                            text: "void setup()\n{\n  size(640, 480);\n  stroke(255);\n  frameRate(90);\n}\n\nfloat y = 100;\nvoid draw()\n{\n  background(0);\n  y = y - 1;\n  if (y < 0) { y = height; }\n  line(0, y, width, y);\n}\n"
                            onCursorRectangleChanged: flick.ensureVisible(cursorRectangle)
                        }
                    }
                }
     
                
                Rectangle {
                    id: runButton
                    anchors.top: code.bottom
                    anchors.topMargin: 10
                    anchors.horizontalCenter: code.horizontalCenter
                    width: 100
                    height: 50
                    border.color: "darkgrey"
                    border.width: 4
                    radius: 10
                    color: "lightgreen"
                    Text {
                        anchors.centerIn: parent
                        font.pixelSize: 24
                        font.bold: true
                        text: "run"
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            mainScreen.state = "Webview";
                            webview.reload.trigger();
                        }
                    }
                }
            } // Ende Item zur Gruppierung von Code und Button
        } // Ende Rectangle mit ID "codeViewGroup"
    } // Ende Item mit ID "codeView"

    WebView {
        id: webview
        opacity: 0
        anchors.fill: parent
        anchors.margins: 0
        url: "index.html"
        javaScriptWindowObjects: QtObject {
            WebView.windowObjectName: "qml"
            function code() {
                return codeEditor.text
            }
        }
        MouseArea {
            anchors.fill: parent
            onPressAndHold: {
                mainScreen.state = "Editor";
            }
        }
    }

    states: [
        State{
            name: "Webview"
            PropertyChanges{
                target: webview
                opacity: 1
                focus: true
            }
            PropertyChanges {
                target: codeView
                opacity: 0
            }
        },
        State {
            name: "Editor"
            PropertyChanges{
                target: webview
                opacity: 0
                focus: false
            }
            PropertyChanges {
                target: codeView
                opacity: 1
            }
        }
    ]

    transitions: [
        Transition {
            PropertyAnimation{
                properties: "opacity"
                duration: 1000
                easing.type: "OutCubic"
            }
        }
    ]

}
