import Qt 4.7

Rectangle {
    id: mainScreen
    width: 800
    height: 600
    color: "black"  
    
    property int targetX: 0
    property int targetY: 0

    Image {
        id: talk
        source: "say.svg"
        sourceSize.width: 236
        sourceSize.height: 214
        
        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 30
            text: "Olá mundo!"
        }
     }

     
    MouseArea {
        id: mouseArea
        anchors.fill: parent
    }    

    states: State {
        name: "clicked"
        when: mouseArea.pressed
        PropertyChanges {
            target: talk
            y: mouseArea.mouseY
            x: mouseArea.mouseX
        }
    }
    
   transitions: Transition {
        NumberAnimation { properties: "x,y"; easing.type: Easing.InOutQuad }
    }
    
}