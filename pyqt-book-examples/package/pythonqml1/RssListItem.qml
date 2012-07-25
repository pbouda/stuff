import Qt 4.7

Item {
    id: rssItem

    property alias text: itemText.text
    property alias date: itemDate.text
    property alias backgroundcolor: rectBackground.color

    signal clicked

    height: itemDate.height + itemText.height + 20
    width: parent.width

    Rectangle {
        id: rectBackground
        anchors.fill: parent
        color: "lightgrey"
        border.color: "darkgrey"
        border.width: 2

        Item {
            Text {
                id: itemDate
                font.pixelSize: 16
            }

            Text {
                id: itemText
                anchors.margins: 10
                anchors.top: itemDate.bottom
                font.pixelSize: 20
                width: 360
                wrapMode: Text.WordWrap
            }
        }

        MouseArea {
            id: mouseRegion
            anchors.fill: parent
            onPressed: rssItem.state = 'Pressed'
            onReleased: rssItem.state = 'Default'
            onClicked: { rssItem.clicked(); }
        }
    }

    states:[
        State {
            name: "Pressed"
            when: mouseRegion.pressed == true
            PropertyChanges {
                target: itemText
                style: Text.Sunken
                color: "white"
            }
        }
    ]

}
