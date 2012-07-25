import Qt 4.7

Rectangle {

    id: mainScreen

    Column {
        id: list
        
        anchors.fill: parent
        spacing: 10
        anchors.margins: 5
        
        Column {
            spacing: 10
            Repeater {
                model: utterances
                delegate: Utterance {}
            }
        }

    }

}