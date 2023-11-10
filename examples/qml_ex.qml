import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.0
import GRWidget 1.0

ApplicationWindow {
  id: mainwindow
  title: "hexbin Demo Application"
  width: 600
  height: 450
  visible: true

  Text {
    id: xy
    font.pointSize: 12
    font.family: "Courier New"
    x: 5
    y: 5
    text: ""
  }

  ColumnLayout {
    id: root
    spacing: 6
    anchors.fill: parent

    RowLayout {
      Layout.fillWidth: true
      Layout.alignment: Qt.AlignCenter

      Text {
        text: "Number of bins:"
      }

      Slider {
        id: nbinsSlider
        implicitWidth: 100
        implicitHeight: 30
        value: 30
        from: 10
        to: 60
        stepSize: 1
        onValueChanged: {
          painter.nbins = nbinsSlider.value;
          painter.update()
        }
      }
    }

    GRWidget {
      id: painter
      Layout.fillWidth: true
      Layout.fillHeight: true

      property int nbins: 30
      property string text: ""

      MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onPositionChanged: (mouse) => {
          xy.text = painter.getXY(mouse.x, mouse.y);
        }
      }
    }
  }
}
