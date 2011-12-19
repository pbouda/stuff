import QtQuick 1.0
import myAngleGraph 1.0

Rectangle {
    id: main
    width: 800
    height: 600

    AngleGraph {
        id: angleGraph01
        width: 1
        height: 1  
        clip: true
    }

}