import Qt 4.7
import QtWebKit 1.0

Rectangle {
    id: mainScreen

    property int currentIndex: 0

    width: 360
    height: 640

    color: "white"

    XmlListModel {
        id: xmlModel
        source: "http://www.mobileqt.de/blogposts.rss"
        query: "/rss/channel/item"

        XmlRole { name: "title"; query: "title/string()" }
        XmlRole { name: "guid"; query: "guid/string()" }
        XmlRole { name: "link"; query: "link/string()" }
        XmlRole { name: "pubDate"; query: "pubDate/string()" }
    }

    ListView {
        id: listviewRss
        anchors.fill: parent
        focus: true
        orientation: ListView.Vertical

        model: xmlModel

        delegate: RssListItem {
            text: title
            date: pubDate
            backgroundcolor: mainScreen.currentIndex == index ? "#9bf" : "lightgrey"
            onClicked: mainScreen.currentIndex = index,
                       webview.url = xmlModel.get(index).link,
                       mainScreen.state = "Webview"
        }
    }

    WebView {
        id: webview
        opacity: 0
        anchors.fill: parent
        MouseArea {
            anchors.fill: parent
            onClicked: mainScreen.state = "Rsslist"
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
                target: listviewRss
                opacity: 0
            }
        },
        State {
            name: "Rsslist"
            PropertyChanges{
                target: webview
                opacity: 0
                focus: false
            }
            PropertyChanges {
                target: listviewRss
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
