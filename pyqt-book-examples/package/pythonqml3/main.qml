import Qt 4.7

Rectangle {
    id: mainScreen
    
    width: 400
    height: 400
    
    signal messageRequested;

    function updateMessage(text) {
        message.text = text
    }
    
    Text {
        id: message
        anchors.top: parent.top
        anchors.bottom: button.top
        width: parent.width
        text: ""
        wrapMode: Text.WordWrap
        font.pixelSize: 30
    }
    
    Rectangle {
        id:button
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        height: 50
        color: "darkgrey"
        Text {
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Aktualisieren"
            color: "white"
            font.pixelSize: 20
        }
        MouseArea {
            anchors.fill: parent
            onClicked: messageRequested()
        }
    }
    
}    
