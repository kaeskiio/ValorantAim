#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>

#include "hidcustom.h"

signed char delta[3] = {0, 0, 0};

struct _MOUSEINFO{
  struct{
    uint8_t bmLeftButton : 1;
    uint8_t bmRightButton : 1;
    uint8_t bmMiddleButton : 1;
    uint8_t bmXButton1 : 1;
    uint8_t bmXButton2 : 1;
    uint8_t bmDummy : 3;
  };
  int8_t dX;
  int8_t dY;
  int8_t dZ;
};

void MouseRptParser::Parse(USBHID *hid, bool is_rpt_id, uint8_t len, uint8_t *buf)
{
  myMouseInfo *pmi = (myMouseInfo *)buf;

  if (CHECK_BIT(prevState.mouseInfo.buttons, leftMouse) != CHECK_BIT(pmi->buttons, leftMouse))
  {
    if (CHECK_BIT(pmi->buttons, leftMouse))
      Mouse.press(leftMouse);
    else
      Mouse.release(leftMouse);
  }

  if (CHECK_BIT(prevState.mouseInfo.buttons, rightMouse) != CHECK_BIT(pmi->buttons, rightMouse))
  {
    if (CHECK_BIT(pmi->buttons, rightMouse))
      Mouse.press(rightMouse);
    else
      Mouse.release(rightMouse);
  }

  if (CHECK_BIT(prevState.mouseInfo.buttons, middleMouse) != CHECK_BIT(pmi->buttons, middleMouse))
  {
    if (CHECK_BIT(pmi->buttons, middleMouse))
      Mouse.press(middleMouse);
    else
      Mouse.release(middleMouse);
  }

  if (CHECK_BIT(prevState.mouseInfo.buttons, previousMouse) != CHECK_BIT(pmi->buttons, previousMouse))
  {
    if (CHECK_BIT(pmi->buttons, previousMouse))
      Mouse.press(previousMouse);
    else
      Mouse.release(previousMouse);
  }

  if (CHECK_BIT(prevState.mouseInfo.buttons, nextMouse) != CHECK_BIT(pmi->buttons, nextMouse))
  {
    if (CHECK_BIT(pmi->buttons, nextMouse))
      Mouse.press(nextMouse);
    else
      Mouse.release(nextMouse);
  }

  if (pmi->dX || pmi->dY)
    OnMouseMove(pmi);

  if (pmi->wheel)
    OnWheelMove(pmi);

  prevState.bInfo[0] = buf[0];
}

void MouseRptParser::OnMouseMove(myMouseInfo *mi)
{
  delta[0] = mi->dX;
  delta[1] = mi->dY;
}

void MouseRptParser::OnWheelMove(myMouseInfo *mi)
{
  delta[2] = mi->wheel;
}

#include <usbhub.h>

USB Usb;
USBHub Hub(&Usb);
HIDBoot<USB_HID_PROTOCOL_MOUSE> HidMouse(&Usb);

MouseRptParser Prs;

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(1);
  Usb.Init();
  HidMouse.SetReportParser(0, &Prs);
  Mouse.begin();
}

void loop()
{
  delta[0] = 0;
  delta[1] = 0;
  delta[2] = 0;
  Usb.Task();\

  if (Serial.available() > 0)
  {
    char inChar = Serial.read();
    if (inChar == 'M')
      Serial.readBytes((char *)&delta, 2);
    else if (inChar == 'C')
      Mouse.click();
  }
  Mouse.move(delta[0], delta[1], delta[2]);
}