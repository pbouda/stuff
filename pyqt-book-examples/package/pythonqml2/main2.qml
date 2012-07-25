import Qt 4.7

Rectangle {
    id: mainScreen

    width: 400
    height: 400

    ListView {
        id: listview
        anchors.fill: parent
        orientation: ListView.Vertical

        model: colorModel

        delegate: Rectangle {
            height: colorText.height + 20
            width: parent.width
            color: modelData.color
            Text {
                id: colorText
                text: modelData.text
                font.pixelSize: 20
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }

}
