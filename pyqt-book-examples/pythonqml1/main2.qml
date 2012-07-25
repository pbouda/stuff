import Qt 4.7

Rectangle {
    id: mainScreen
    
    XmlListModel {
        id: xmlModel
        source: "http://www.dasskript.com/blogposts.rss"
        query: "/rss/channel/item"

        XmlRole { name: "title"; query: "title/string()" }
        XmlRole { name: "guid"; query: "guid/string()" }
        XmlRole { name: "link"; query: "link/string()" }
        XmlRole { name: "pubDate"; query: "pubDate/string()" }
    }

    Column {
        id: listviewRss
        anchors.fill: parent
        spacing: 10
        focus: true
        Repeater {
            model: xmlModel
    
            delegate: RssListItem2 {
                text: title
                date: pubDate
                onClicked: console.log(link)
            }
        }
    }


}
