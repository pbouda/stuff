import Qt 4.7

Rectangle {
    id: mainScreen

    property int currentIndex: 0

    width: 400
    height: 400

    color: "white"

    ListView {
        id: listview
        anchors.fill: parent
        orientation: ListView.Vertical

        model: colorModel

        delegate: Rectangle {
            height: colorText.height + 20
            width: parent.width
            color: modelData
            Text {
                id: colorText
                text: modelData
                font.pixelSize: 20
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }

}
