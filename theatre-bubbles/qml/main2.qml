import Qt 4.7

Rectangle {
    id: mainScreen
    width: 800
    height: 600
    color: "black"  
    
    Repeater {
        model: modelFaces

        Image {
            id: talk
            source: "say.svg"
            sourceSize.width: 236
            sourceSize.height: 214
            x: modelData[0]
            y: modelData[1]
            
            Text {
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                font.pixelSize: 30
                text: "Olá mundo!"
            }
        }
    }
    
}