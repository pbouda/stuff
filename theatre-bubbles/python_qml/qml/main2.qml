import Qt 4.7
import Qt.labs.particles 1.0


Rectangle {
    id: mainScreen
    width: 1024
    height: 768
    color: "black"
    focus: true
    
    property int lastX : 0
    property int lastY : 0
    property int lastDiff : 0

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        onPositionChanged: {
            var diff = (lastX - mouse.x);
            //console.log(diff);
            think1.x -= diff;
            if ( (lastDiff > 0) && (diff < 0) ) {
                think1TurnBubbleLeft.start();
            }
            //if ( (lastDiff < 0) && (diff > 0) ) {
            //    think1TurnBubbleRight.start();
            //}
            //think1.width = (200 - diff*3);
            lastX = mouse.x;
            if (diff != 0) {
                lastDiff = diff
            }
        }
        onPressed: {
            lastX = mouse.x;
        }
        onReleased: {
            think1.width = 200;
        }
    }


    Image {
        id: think1
        source: "think3.png"
        x: 400
        y: 800
        
        Text {
            anchors.top: parent.top
            anchors.topMargin: 30
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 60
            font.bold: false
            font.family: "Ravie"
            text: "???"
        }
        
        states: State {
            name: "moved"; when: mouseArea.pressed
        }
         
        transitions: Transition {
            NumberAnimation { properties: "x"; easing.type: Easing.InOutQuad }
        }
     
    }
    
    Image {
        id: think2
        source: "think6.png"
        x: 260
        y: 800
        
        Text {
            anchors.top: parent.top
            anchors.topMargin: 40
            anchors.leftMargin: 10
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 35
            font.bold: false
            font.family: "Ravie"
            text: " Este\nsujeito\n  é um\nelitista."
        }

    }

    Image {
        id: think3
        source: "think5.png"
        x: 120
        y: 800
        
        Text {
            anchors.top: parent.top
            anchors.topMargin: 100
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 50
            font.bold: false
            font.family: "Ravie"
            text: "BOUM??"
        }

    }

    Image {
        id: think4
        source: "think7.png"
        x: 260
        y: 800
        
        Text {
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.topMargin: 80
            anchors.leftMargin: 120
            //anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 35
            font.bold: false
            font.family: "Ravie"
            text: "       Safa,\nque esta é das\n fantásticas..."
        }

    }

    Particles {
        id: particles
        
        source: "star2.png";
   
        width: 1; height: 1
        anchors.centerIn: think2
   
        emissionRate: 0
        lifeSpan: 600
        lifeSpanDeviation: 400
        angle: 0
        angleDeviation: 360
        velocity: 350
        velocityDeviation: 700
    }
    
    Particles {
        id: particles2
        
        source: "star3.png";
   
        width: 1; height: 1
        anchors.centerIn: think3
   
        emissionRate: 0
        lifeSpan: 600
        lifeSpanDeviation: 400
        angle: 0
        angleDeviation: 360
        velocity: 350
        velocityDeviation: 700
    }
    
    Image {
        id: buddha
        source: "buddha2.png"
        opacity: 0
        //anchors.centerIn: parent
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.leftMargin: 200
        anchors.topMargin: 120
    }

    Image {
        id: bat
        source: "bat2.png"
        opacity: 0
        x: 600
        y: 100
    }

    Keys.onPressed: {
        if (event.key == Qt.Key_1) {
            console.log('Key 1 was pressed');
            event.accepted = true;
            think1Animation1.start();
        }
        else if (event.key == Qt.Key_2) {
            console.log('Key 2 was pressed');
            event.accepted = true;
            think1Animation5.start();
        }
        else if (event.key == Qt.Key_3) {
            console.log('Key 3 was pressed');
            event.accepted = true;
            think1Animation3.start();
        }
        else if (event.key == Qt.Key_4) {
            console.log('Key 4 was pressed');
            event.accepted = true;
            think1Animation4.start();
        }
        else if (event.key == Qt.Key_5) {
            console.log('Key 5 was pressed');
            event.accepted = true;
            think1Animation5.start();
        }
        else if (event.key == Qt.Key_Q) {
            console.log('Key Q was pressed');
            event.accepted = true;
            think2Animation1.start();
        }
        else if (event.key == Qt.Key_W) {
            console.log('Key w was pressed');
            event.accepted = true;
            think2Animation2.start();
        }
        else if (event.key == Qt.Key_A) {
            console.log('Key A was pressed');
            event.accepted = true;
            think3Animation1.start();
        }
        else if (event.key == Qt.Key_S) {
            console.log('Key S was pressed');
            event.accepted = true;
            think3Animation2.start();
        }
        else if (event.key == Qt.Key_U) {
            console.log('Key U was pressed');
            event.accepted = true;
            think4Animation1.start();
        }
        else if (event.key == Qt.Key_I) {
            console.log('Key I was pressed');
            event.accepted = true;
            think4Animation2.start();
        }
        else if (event.key == Qt.Key_Y) {
            console.log('Key Y was pressed');
            event.accepted = true;
            buddhaAnimation1.start();
        }
        else if (event.key == Qt.Key_X) {
            console.log('Key X was pressed');
            event.accepted = true;
            buddhaAnimation2.start();
        }
        else if (event.key == Qt.Key_N) {
            console.log('Key N was pressed');
            event.accepted = true;
            batAnimation1.start();
        }
        else if (event.key == Qt.Key_M) {
            console.log('Key M was pressed');
            event.accepted = true;
            batAnimation2.start();
        }
    }    

    ParallelAnimation {
        id: think1Animation1
        SpringAnimation { target: think1; property: "y"; from: 800; to: 250; spring: 0.7; damping: 0.1 }
        SequentialAnimation {
            PropertyAnimation { target: think1; property: "height"; to: 150; duration: 500; }            
            PropertyAnimation { target: think1; property: "height"; to: 207; duration: 500; }            
        }
    }
    
    ParallelAnimation {
        id: think1Animation2
        SpringAnimation { target: think1; property: "y"; from: 800; to: 250; spring: 0.7; damping: 0.1 }
        SequentialAnimation {
            PropertyAnimation { target: think1; property: "height"; to: 150; duration: 500; }            
            PropertyAnimation { target: think1; property: "height"; to: 207; duration: 500; }            
        }
    }

    ParallelAnimation {
        id: think1Animation3
        SpringAnimation { target: think1; property: "x"; from: 500; to: 200; spring: 0.3; damping: 0.2 }
        SequentialAnimation {
            PropertyAnimation { target: think1; property: "width"; to: 250; duration: 500; }            
            PropertyAnimation { target: think1; property: "width"; to: 200; duration: 500; }
        }
    }
    
    ParallelAnimation {
        id: think1Animation4
        SpringAnimation { target: think1; property: "x"; from: 200; to: 500; spring: 0.3; damping: 0.2 }
        SequentialAnimation {
            PropertyAnimation { target: think1; property: "width"; to: 150; duration: 500; }            
            PropertyAnimation { target: think1; property: "width"; to: 200; duration: 500; }
        }
    }
    
    PropertyAnimation {
        id: think1Animation5
        target: think1
        property: "opacity"
        to: 0
        duration: 1000
        easing.type: "OutCubic"
    }

    SpringAnimation {
        id: think1TurnBubbleLeft
        target: think1
        property: "width"
        from: 200
        to: -200
        spring: 3.0
        damping: 0.2
    }

    SpringAnimation {
        id: think1TurnBubbleRight
        target: think1
        property: "width"
        from: -200
        to: 200
        spring: 3.0
        damping: 0.2
    }

    ParallelAnimation {
        id: think2Animation1
        SpringAnimation { target: think2; property: "y"; from: 800; to: 50; spring: 0.7; damping: 0.1 }
        SequentialAnimation {
            PropertyAnimation { target: think2; property: "height"; to: 300; duration: 500; }            
            PropertyAnimation { target: think2; property: "height"; to: 414; duration: 500; }
        }
    }

    SequentialAnimation {
        id: think2Animation2
        ParallelAnimation {
            ScriptAction { script: particles.burst(2000); }
            PropertyAnimation { target: think2; property: "opacity"; to: 0; duration: 500; easing.type: "OutCubic"; }
        }
        //PauseAnimation { duration: 1000 }
        //PropertyAnimation { target: think2; property: "y"; to: 800; duration: 100; }
        //PropertyAnimation { target: think2; property: "opacity"; to: 1; duration: 100; }
    }

    ParallelAnimation {
        id: think3Animation1
        SpringAnimation { target: think3; property: "y"; from: 800; to: 200; spring: 0.7; damping: 0.1 }
        SequentialAnimation {
            PropertyAnimation { target: think3; property: "height"; to: 300; duration: 500; }            
            PropertyAnimation { target: think3; property: "height"; to: 362; duration: 500; }
        }
    }

    ParallelAnimation {
        id: think3Animation2
        ScriptAction { script: particles2.burst(2000); }
        PropertyAnimation { target: think3; property: "opacity"; to: 0; duration: 500; easing.type: "OutCubic" }
    }
    

    ParallelAnimation {
        id: think4Animation1
        SpringAnimation { target: think4; property: "y"; from: 800; to: 50; spring: 0.7; damping: 0.1 }
        SequentialAnimation {
            PropertyAnimation { target: think4; property: "height"; to: 450; duration: 500; }            
            PropertyAnimation { target: think4; property: "height"; to: 500; duration: 500; }
        }
    }

    ParallelAnimation {
        id: think4Animation2
        //ScriptAction { script: particles2.burst(2000); }
        PropertyAnimation { target: think4; property: "opacity"; to: 0; duration: 500; easing.type: "OutCubic" }
    }

    NumberAnimation { id: buddhaAnimation1; target: buddha; property: "opacity"; from: 0.0; to: 0.9; duration: 2000;  easing { type: Easing.OutBack; } }    
    PropertyAnimation { id: buddhaAnimation2; target: buddha; property: "opacity"; to: 0; duration: 2000;  easing { type: Easing.InBack; }  }

    ParallelAnimation {
        id: batAnimation1;
        NumberAnimation {  target: bat; property: "opacity"; from: 0.0; to: 0.9; duration: 2000; }    
        PropertyAnimation {  target: bat; property: "x"; from: -600; to: 0; duration: 1500;  easing { type: Easing.OutBack; } }    
    }
    
    PropertyAnimation { id: batAnimation2; target: bat; property: "opacity"; to: 0; duration: 1000;  easing { type: Easing.InBack; }  }
}