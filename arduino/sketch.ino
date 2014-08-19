/*
 * 
 */
// DEFINE PINS
#define TXPIN        2
#define RXPIN        3
#define LIGHTSENSOR  0
#define TEMPERATURESENSOR   1
#define SOUNDSENSOR  2
#define WHITELED     5
#define REDLED       6
#define BUZZER       4
#define BUTTON       7

 // DEFINE TRANSMITTER
#include <NewRemoteTransmitter.h>
#include <NewRemoteReceiver.h>

#define REMOTECODE   123
// Create a Transmitter on address 123, using digital pin 11 to transmit, 
// with a period duration of 260ms (default), repeating the transmitted
// code 2^3=8 times.
NewRemoteTransmitter Transmitter(REMOTECODE, TXPIN, 260, 1);
boolean SwitchState[15];

// DEFINE LIGHT VARIABLE
char LightEffectNumber = 0;
float TempoPic = 0.0;
#define MAXTEMPO 2.5
#define MOYTEMP 1.0
#define MINTEMPO 0.7

const struct HeartArray_s {
  unsigned long HeartDelay;
  int HeartPulse;
  int HeartVariation;
}
HeartArray[] = { {60, 0, 0}, {100, 180, 50}, {30, 0 , 0}, {800, 100, 10}};
char HeartIndex = 1;   // this initialization is important or it starts on the "wrong foot"
unsigned long PreviousHeartMillis;

// DEFINE ERRORS
#define WAITTOSENDDERROR   -1
#define NOERROR            0
#define PARSEERROR         1
#define COMMANDERROR       2
#define ARGUMENTERROR      3
#define TOOLONGERROR       4
#define UNKOWCOMMANDERROR  5
// END DEFINE ERROR

#define MAXBUFFSIZE        25
const struct CommandList_s
{
  char     Command[MAXBUFFSIZE];
  int      (*f)(char *Arg);
  boolean  IsNum;
} Commandlist[] = {
  {"switchon",           SwitchOn,          true },
  {"switchoff",          SwitchOff,         true },
  {"switchallon",        SwitchAllOn,       true },
  {"switchalloff",       SwitchAllOff,      true },
  {"switchstate",        GetSwitchState,    true },
  {"learn",              Learn,             true },
  {"tempopic",           SetTempoPic,       true },  
  {"notification",       Notification,      true },
  {"alarm",              Alarm,             true },
  {"lightsensor",        LightSensor,       true },
  {"lightmoysensor",     LightMoySensor,    true },  
  {"soundsensor",        SoundSensor,       true },
  {"soundmoysensor",     SoundMoySensor,    true },  
  {"temperaturesensor",  TemperatureSensor, true },
  {"ping",               Ping,              true },
  {"sleep",              Sleep,             true },  
  {"wakeup",             WakeUp,            true },  
  {"lighteffect",        LightEffect,       true },
  {"",                   NULL,              true }
};


// NOTIFICATION
char NotificationPriority;

//SLEEP MODE
boolean SleepMode = false;
// SENSOR
float Temperature = 0.0;
unsigned int Light = 0;
unsigned int CalculateLightMoy = 0;
unsigned int LightMoy = 0;
unsigned char LightMoyIndex = 0;


int LastSound = 0;
int Sound = 0;
#define  MOYNUMBER  255
unsigned int CalculateSoundMoy = 0;
unsigned int SoundMoy = 0;
unsigned char SoundMoyIndex = 0;

void setup() 
{ 
  pinMode(WHITELED, OUTPUT);
  pinMode(REDLED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  
  pinMode(BUTTON, INPUT);
  pinMode(LIGHTSENSOR, INPUT);
  pinMode(TEMPERATURESENSOR, INPUT);
  pinMode(RXPIN, INPUT);
  
  NotificationPriority = 0;
  PreviousHeartMillis = millis();
  //NewRemoteReceiver::init(RXPIN, 2, ShowCode);
  for (int i = 0; i < 15; i++)
    SwitchState[i] = 0;
  Serial.begin(9600);
  while(!Serial)
  {
    SendLightValue(255, 0, 0, 0);
    delay(500);
    SendLightValue(0, 255, 0, 0);
    delay(500);
  }
  GetSensorValues(true);
  LightMoy = Light;
  SoundMoy = Sound;
  Serial.println("setup done");
}

// INTERRUPT FOR TRANSMITTER RECEIVING
void ShowCode(NewRemoteCode ReceivedCode) {
  // Note: interrupts are disabled. You can re-enable them if needed.
  Serial.print("received:");
  // Print the received code.
  Serial.print("remote:");
  Serial.print(ReceivedCode.address);

  if (ReceivedCode.groupBit) {
    Serial.print(":group:");
  } 
  else {
    Serial.print(":unit:");
    Serial.print(ReceivedCode.unit);
  }

  switch (ReceivedCode.switchType) {
    case NewRemoteCode::off:
      Serial.print(":off");
      break;
    case NewRemoteCode::on:
      Serial.print(":on");
      break;
    case NewRemoteCode::dim:
      Serial.print(":dim");
      break;
  }

  if (ReceivedCode.dimLevelPresent) {
    Serial.print(":dim level:");
    Serial.print(ReceivedCode.dimLevel);
  }

  Serial.print(":period:");
  Serial.print(ReceivedCode.period);
  Serial.println("us.");
}

// MAIN LOOP
unsigned long CurrentMillis = 0;
  char BufferPos = 0; // position in read Buffer
  boolean ParsingCommand = true; 
void loop()
{
  boolean CommandAvailable;
  char Command[MAXBUFFSIZE];
  char Argument[MAXBUFFSIZE];
  
  CurrentMillis = millis();
  // check if data arrived in the Serial Buffer
  if (Serial.available() > 0)
  {
    if (BufferPos == 0 && ParsingCommand == true)
    {
      Command[0] = '\0';
      Argument[0] = '\0';
    }
    CommandAvailable = GetCommand(Command, Argument);
  }
  LightLed();
  ReadButton();
  if (CommandAvailable == true)
  {
    ExecCommand(Command, Argument);
    CommandAvailable = false;
  }
  if (SleepMode == false)
    SendNotification();
  SendLearning();
  GetSensorValues(false);
}

// Command parsing
void ExecCommand(char *Cmd, char *Arg)
{
  int CommandError = UNKOWCOMMANDERROR;    
 
  for (int i = 0 ; Commandlist[i].Command[0] != '\0' ; i++)
    if (!strncmp(Cmd, Commandlist[i].Command, MAXBUFFSIZE))
    {
      if (CheckString(Arg, Commandlist[i].IsNum) == true)
       CommandError = Commandlist[i].f(Arg);          
      else
        CommandError = PARSEERROR;
      break;
    }
  if (CommandError != WAITTOSENDDERROR)
    SendError(Cmd, Arg, CommandError);
}

// Send CommandError
void SendError(char *cmd, char *arg, int err)
{
  if (err == 0)
  {
    Serial.print("OK:");
    Serial.print(cmd);
    Serial.print(":");
    Serial.println(arg);
  }
  else
  {
    Serial.print("ERROR:");
    Serial.print(cmd);
    Serial.print(":");
    Serial.print(arg);
    Serial.print(":");
    Serial.println(err);
  }
}

// Read Serial Buffer to get Commands and Arguments
boolean GetCommand(char *Command, char *Argument)
{
  if (Serial.available() == 0)
    return false;
    // read the incoming byte: 
  char InByte = Serial.read();
  if (BufferPos < MAXBUFFSIZE)    
    switch (InByte)
    { 
      case '\r':
        return false;
      case '\n':
        if (ParsingCommand == true)
          Command[BufferPos] = '\0';
        else
          Argument[BufferPos] = '\0';
        BufferPos = 0;  
        ParsingCommand = true;
        return true;
      case ':':
        ParsingCommand = false;
        Command[BufferPos] = '\0';
        BufferPos = 0;
        return false;
      default:
        if (ParsingCommand == true)
          Command[BufferPos++] = InByte;
        else
          Argument[BufferPos++] = InByte;
        return false;
    }
  else
  {
    while (Serial.available() > 0)
      Serial.read();
    BufferPos = 0;
    Command[0] = '\0';
    Argument[0] = '\0';
    SendError("", "", TOOLONGERROR);
  }
  return false;
}

boolean CheckString(char *s, boolean isnum)
{
  for(int i = 0; s[i] != '\0'; i++)
    if (isnum == true && (isdigit(s[i]) ==  0 && s[i] != '.' && s[i] != '-' ))
      return false;
    else
      if (isnum == false && (s[i] < 'a' || s[i] > 'z'))
        return false;
  return true;
}

// LIGHT
int SetTempoPic(char *Arg)
{
  float P = atof(Arg);
  
  if (P < -0.5 || P > 1.5)
    return ARGUMENTERROR;
  TempoPic = P;
  return NOERROR;
}

void LightLed()
{
  if (SleepMode == true)
   { 
     SendLightValue(0, 0, 0, 0);
     return;
   }
   if (NotificationPriority != 0)
     return;
   switch (LightEffectNumber)
   {
     case 1: //Continue
       ContinueEffect();
       break;
     case 2: //Wave
       WaveEffect();
       break;
     case 0:
     default:
       LightEffectNumber = 0;
       HumanEffect();
       break;
   }   
}

void ContinueEffect()
{  SendLightValue(255, 255, 0, 0); }

void WaveEffect()
{
  float Periode = 120000.0;
  float Radian = 2.0 * PI * ((float)CurrentMillis / Periode);
  float WhiteValue = 128 + 128.0 * sin(Radian);
  float RedValue = 128 + 128.0 * sin(Radian + PI);
  SendLightValue(WhiteValue, RedValue, 0, 0);    
}
void HumanEffect() 
{
  float Tempo = 0.0;
  float TempoObjectif;
  unsigned char WhiteValue = 0;
  unsigned char RedValue = 0;
  
  GetSoundSensor();
  if (abs(LastSound - Sound) > 500 && Tempo <= 2)
  {
    if (TempoPic > 0.25)
      TempoPic *= 1.1;
    else 
      TempoPic += 0.25;
  }
  if (TempoPic > 1.5)
    TempoPic = 1.5;
  else if (TempoPic < -0.4)
    TempoPic = -0.4;

  TempoObjectif = 1.000 + 0.100 * sin(2 * PI * CurrentMillis/600000) + 0.05 * ((Temperature - 20) / 200 + ((float)LightMoy - 200) / 200);

  if (-0.05 < TempoPic && TempoPic < 0.05)
    TempoPic = 0;
  else
    TempoPic = TempoPic * 0.99999;
    
  Tempo = TempoObjectif + TempoPic;
  float Periode = 5000.0 / (Tempo * Tempo);
  float Radian = 2.0 * PI * ((float)CurrentMillis / Periode);
  WhiteValue = 128 + (100.0 * sin(Radian)) - 17 * (MOYTEMP - Tempo);
//HEART
  if ((CurrentMillis < PreviousHeartMillis) || (CurrentMillis - PreviousHeartMillis) >= (unsigned long)(HeartArray[HeartIndex].HeartDelay / Tempo))
  {
    RedValue = HeartArray[HeartIndex].HeartPulse - HeartArray[HeartIndex].HeartVariation * (MOYTEMP - Tempo);
    if (++HeartIndex == 4)
      HeartIndex = 0;
    PreviousHeartMillis = CurrentMillis;
  }
  SendLightValue(WhiteValue, RedValue, 0, 0);
}

void SendLightValue(int White, int Red, int Green, int Blue)
{
  if (White >=0) 
    analogWrite(WHITELED, White);
  if (Red >=0) 
    analogWrite(REDLED, Red);
 /* if (Green >=0) 
    analogWrite(GREENLED, Green);
   if (Blue >=0) 
    analogWrite(BLUELED, Blue);*/
}
int LightEffect(char *Arg)
{ 
  LightEffectNumber = atoi(Arg);
  if (LightEffectNumber < 0 || LightEffectNumber > 2)
    return ARGUMENTERROR;
  return NOERROR; 
}

// READ BUTTON
unsigned long ButtonPrevioustMillis = 0;
boolean ButtontState = false;
boolean ButtontLastState = false;
boolean ReadingButtontState = false;
int LongCountButton = 0;
int ShortCountButton = 0;

void ReadButton()
{
  ButtontState = digitalRead(BUTTON);
  if (ButtontState == true)
  {
    if (NotificationPriority == 4) // RESET ALARM
      ResetNotification();
      
     if (TempoPic > 0.5)
       TempoPic *= 1.1;
     else 
       TempoPic += 0.5;
     ReadingButtontState = true;
     if (ButtontLastState == false)          
       {
         ButtontLastState = true;
         ButtonPrevioustMillis = CurrentMillis;
       }
  }
  if (ReadingButtontState == true)
  {
    if(ButtontState == false && ButtontLastState == true)
    { 
      if (CurrentMillis - ButtonPrevioustMillis < 500)
        ShortCountButton++;
      else
        LongCountButton++;
      ButtonPrevioustMillis = CurrentMillis;
      ButtontLastState = false;
      
    }
    if ((CurrentMillis < ButtonPrevioustMillis) || (ButtontState == false && CurrentMillis - ButtonPrevioustMillis > 1000))
    {
      Serial.print("button:");
      Serial.print(ShortCountButton, DEC);
      Serial.print(":"); 
      Serial.println(LongCountButton, DEC);
      ActionButton();
      ButtonPrevioustMillis = 0;
      LongCountButton = 0;
      ShortCountButton = 0;
      ReadingButtontState = false; 
    }
  }  
}

void ActionButton()
{
  switch (LongCountButton)
  {
    case 1 :
      if (ShortCountButton == 0)
        SwitchAllOn("");
      else
        Switch(ShortCountButton, true);
      break;
    case 2 :
      if (ShortCountButton == 0)
        SwitchAllOff("");
      else
        Switch(ShortCountButton, false);
      break;
    default:
      if (ShortCountButton == 0)
        Serial.println("no action");
      break;
  }
  if (LongCountButton == 0)
    switch (ShortCountButton)
    {
      case 1 :
        if (++LightEffectNumber > 2)
          LightEffectNumber = 0;
        break;
      case 2 :
        if (SleepMode == true)
          WakeUp("");
        else
          Sleep("");
        break;
      default:
        Serial.println("no action");
        break;
    }
}

// REMOTE SWITCHING
int SwitchOn(char * Arg)
{ return Switch(atoi(Arg), true); }
int SwitchOff(char * Arg)
{ return Switch(atoi(Arg), false); }

int  SwitchAllOn(char * Arg)
{ 
  for (int i = 0; i < 15; i++)
    Switch(i, true);
  return NOERROR;
}
int SwitchAllOff(char * Arg)
{ 
  for (int i = 0; i < 15; i++)
    Switch(i, false);
  return NOERROR;
}

boolean Learning = false;
unsigned long PreviousLearningMillis = 0;

int RemoteLearning = 0;
int Learn(char * Arg)
{ 
  RemoteLearning = atoi(Arg);
  PreviousLearningMillis = CurrentMillis;
  Learning = true; 
  return WAITTOSENDDERROR;
}

void SendLearning()
{
  if (Learning == false)
    return;
  
  Switch(RemoteLearning, true);
  if (CurrentMillis <  PreviousLearningMillis || CurrentMillis < PreviousLearningMillis || CurrentMillis - PreviousLearningMillis > 2000)
  { 
    Learning = false;
    char LearningValue[10];
    SendError("learn", itoa(RemoteLearning, LearningValue, 10), 0);
  }
}

int Switch(char Remote, boolean State)
{
  if (Remote < 0 || Remote > 15)
    return ARGUMENTERROR; 
  SwitchState[Remote] = State;
  for (int i = 0; i < 8; i++)
  {
    CurrentMillis = millis();
    LightLed(); 
    Transmitter.sendUnit(Remote, State);
  }
  return NOERROR;
}

int GetSwitchState(char * Arg)
{
  int Remote = atoi(Arg);
  
  if (Remote < 0 || Remote > 15)
    return ARGUMENTERROR; 
  Serial.print("switch:");
  Serial.print(Remote, DEC);
  Serial.print(":");
  Serial.println(SwitchState[Remote]);
  return NOERROR;
}

// SENSORS

void GetLightSensor()
{ 
  Light = analogRead(LIGHTSENSOR); 
 
  CalculateLightMoy += Light;
  if (LightMoyIndex >= MOYNUMBER)
  {   
    LightMoyIndex = 0;
    LightMoy = CalculateLightMoy / MOYNUMBER;
    CalculateLightMoy = 0;
  }
}

int LightMoySensor(char * Arg)
{ return SendValue("lightmoy", LightMoy); }

int LightSensor(char * Arg)
{ return SendValue("light", Light); }

void GetSoundSensor()
{ 
  LastSound = Sound;
  Sound = analogRead(SOUNDSENSOR); 
  CalculateSoundMoy += Sound;
  if (SoundMoyIndex >= MOYNUMBER)
  {   
    SoundMoyIndex = 0;
    SoundMoy = CalculateSoundMoy / MOYNUMBER;
    CalculateSoundMoy = 0;
  }
}

int SoundMoySensor(char * Arg)
{ return SendValue("soundmoy", SoundMoy); }

int SoundSensor(char * Arg)
{ return SendValue("sound", Sound); }

void GetTemperatureSensor()
{ 
  int Value = analogRead(TEMPERATURESENSOR); 
  float Resistance = (float)(1023 - Value) * 10000 / Value; //get the resistance of the sensor;
  Temperature = 1 / (log(Resistance / 10000) / 3975 + 1 / 298.15) - 273.15;//convert to temperature via datasheet 
}

int TemperatureSensor(char * Arg)
{ return SendValue("temperature", Temperature); }

int SendValue(char *Sensor, float Value)
{
  Serial.print(Sensor);
  Serial.print(":");
  Serial.println(Value);
  return NOERROR;
}

unsigned long PreviousSensorMillis = 0;
void GetSensorValues(boolean Force)
{
  if (Force == true || CurrentMillis < PreviousSensorMillis || (CurrentMillis - PreviousSensorMillis) > 500) 
  {
    PreviousSensorMillis = CurrentMillis;
    GetLightSensor();
    GetSoundSensor();
    GetTemperatureSensor();
  }
}

// PING
int Ping(char * Arg)
{
  Serial.println("pong");
  return NOERROR;
}

int Sleep(char * Arg)
{
  SleepMode = true;
  ResetNotification();
  TempoPic = 0;
  Serial.println("good night");
  return NOERROR;
}

int WakeUp(char * Arg)
{
  SleepMode = false;
  Serial.println("hello");
  return NOERROR;
}

// ALARM
int Alarm(char * Arg)
{
  if (NotificationPriority != 0)
    ResetNotification();
  NotificationPriority = 4;
  return NOERROR;
}

// NOTIFICATION
int Notification(char * Arg)
{
  int NewNotificationPriority = (Arg[0] == '\0' ? 1 : atoi(Arg));
  
  if (NewNotificationPriority < 0 || NewNotificationPriority > 3)
    return ARGUMENTERROR;
  if (NewNotificationPriority < NotificationPriority)
    return WAITTOSENDDERROR;
  if (NotificationPriority != 0)
    ResetNotification();
    
  NotificationPriority = NewNotificationPriority;  
  return NOERROR;
}

boolean NotificationState = false;
unsigned long NotificationStateMillis = 0;
unsigned long PreviousNotificationMillis = 0;
void SendNotification()
{
  if (NotificationPriority == 0)
    return;
  if (PreviousNotificationMillis == 0)
    PreviousNotificationMillis = CurrentMillis;
  
  if (NotificationPriority < 4)
  {
    if (CurrentMillis - NotificationStateMillis > (NotificationState == HIGH ? 25 : 100))
    {
      NotificationState = NotificationState == HIGH ? LOW : HIGH;
      NotificationStateMillis = CurrentMillis;
    
      if (NotificationPriority > 1 && CurrentMillis - PreviousNotificationMillis < 500 * NotificationPriority)
        digitalWrite(BUZZER, NotificationState);
      else
        digitalWrite(BUZZER, LOW);
      SendLightValue(NotificationState == true ? 255 : 0, -1, -1, -1);  
    }
  }
  else
  {
    digitalWrite(BUZZER, HIGH);
    SendLightValue(255, -1, -1, -1);
  }
  
  if (CurrentMillis < NotificationStateMillis || CurrentMillis - PreviousNotificationMillis > 5000 * NotificationPriority)
    ResetNotification();
}

void ResetNotification()
{
  digitalWrite(BUZZER, LOW);
  NotificationState = 0;
  NotificationPriority = 0;
  PreviousNotificationMillis = 0;
}

