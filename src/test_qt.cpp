#include "ros/ros.h"
#include "mainwindow.h"
#include <QApplication>

#include <QThread>
#include <QDebug>

int main(int argc, char **argv)
{

  ros::init(argc, argv, "talker");
  ros::NodeHandle n;
  QApplication a(argc, argv);
  
  qDebug() << QThread::currentThreadId() << "QApplication::exec()を実行するスレッド";
  
  MainWindow w;
  w.show();
  
  return a.exec();
}


/*
#include <sstream>
//#include <qapplication.h>
//#include <qwidget>
#include <QWidget>
#include <QApplication>
#include <QTextEdit>
#include <QtGui>
#include <QObject>
#include <QVBoxLayout>


class MyWindow 
  : public QWidget
{

public:
  MyWindow();
  void changeTest();

private:
  QLabel *my_label;
  QPushButton *my_button;
};

MyWindow::MyWindow()
{
  this->setWindowTitle("hajimete no Qt");
  this->setMaximumSize(500,300);
  this->setMinimumSize(250,150);
  this->resize(400,240);

  
  QPushButton *my_button = new QPushButton("Quit", this);
  my_button->setGeometry(150,100,100,50);
  my_button->setFont(QFont("Times", 20, QFont::Bold));

  QLabel *my_label = new QLabel(this);
  my_label->setFrameStyle( QFrame::Panel | QFrame::Sunken );
  my_label->setText("Hello World.\nIt's fun to creat a program.");
  my_label->setAlignment(Qt::AlignVCenter | Qt::AlignHCenter);
  my_label->setGeometry(50,10,300,50);
  

  QVBoxLayout *layout = new QVBoxLayout;
  QSlider *slider = new QSlider(Qt::Horizontal);
  layout->addWidget(slider);



  QPushButton *button = new QPushButton("Close");
  layout->addWidget(button);
  setLayout(layout);

  // MyObject *ob1 = new MyObject();
  //ob1->setObjectName("object 1"); 

  connect(slider, SIGNAL(valueChanged()), this, &changeTest());
}

void MyWindow::changeTest(int num)
{
  std::cout <<"test"<<std::endl;
}

int main(int argc, char **argv)
{

  ros::init(argc, argv, "talker");
  ros::NodeHandle n;

  QApplication window(argc, argv);

  MyWindow *mainwindow = new MyWindow();

  mainwindow->show();
  return window.exec();
}

*/
