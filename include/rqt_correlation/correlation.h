#ifndef rqt_correlation__ImageView_H
#define rqt_correlation__ImageView_H

#include <rqt_gui_cpp/plugin.h>

/*
#include <ui_image_view.h>
#include <image_transport/image_transport.h>
#include <ros/macros.h>
#include <sensor_msgs/Image.h>
#include <opencv2/core/core.hpp>
*/

#include <QList>
#include <QString>
#include <QSize>
#include <QWidget>

#include <vector>

namespace rqt_correlation {

class Correlation
  : public rqt_gui_cpp::Plugin
{

  Q_OBJECT

public:

  Correlation();

  virtual void initPlugin(qt_gui_cpp::PluginContext& context);

  virtual void shutdownPlugin();

  virtual void saveSettings(qt_gui_cpp::Settings& plugin_settings, qt_gui_cpp::Settings& instance_settings) const;

  virtual void restoreSettings(const qt_gui_cpp::Settings& plugin_settings, const qt_gui_cpp::Settings& instance_settings);
  
  protected slots:
    
    virtual void updateTopicList();
  
 protected:
  
  // deprecated function for backward compatibility only, use getTopics() instead
  ROS_DEPRECATED virtual QList<QString> getTopicList(const QSet<QString>& message_types, const QList<QString>& transports);
  
  virtual QSet<QString> getTopics(const QSet<QString>& message_types, const QSet<QString>& message_sub_types, const QList<QString>& transports);
  
  virtual void selectTopic(const QString& topic);
  
  protected slots:
    
    virtual void onTopicChanged(int index);
  
  virtual void onZoom1(bool checked);
  
  virtual void onDynamicRange(bool checked);
  
  virtual void saveImage();
  
 protected:
  
  virtual void callbackImage(const sensor_msgs::Image::ConstPtr& msg);
  
  //Ui::ImageViewWidget ui_;
  
  QWidget* widget_;
  
  //image_transport::Subscriber subscriber_;
  
  //cv::Mat conversion_mat_;
  
 private:
  
  QString arg_topic_name;
  
};
 
}

#endif // rqt_image_view__ImageView_H
