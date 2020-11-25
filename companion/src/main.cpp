#include <Adafruit_NeoPixel.h>
#include <ArduinoJson.h>

int pin         = 9;
//int cupPixels = 12;
//int bottlePixels   = 70;
//int totalPixels = cupPixels + bottlePixels;
int totalPixels = 70;
int bottleCount = 10;
int pixelsPerBottle = totalPixels / bottleCount;
// message = "";
int totalLocations = totalPixels * 255; //(17850)
int bottleLocations[] = {450, 2300, 4075, 6000, 7800, 9600, 11400, 13350, 15100, 17000};
int flow = -1;
int flowDirection = 1;

int pixelFormat = NEO_GRB + NEO_KHZ800;
Adafruit_NeoPixel *pixels;
DynamicJsonDocument doc(512);

void do_highlight(int location, long color, int spread){
  if(location < 1){
    location = 1;
  } else if(location > totalLocations){
    location = totalLocations;
  }
  int lower = location / 255;
  int upper = lower + 1;

  // Extract the brightness values from the locations
  int lower_brightness = (255 * upper) - location;
  int upper_brightness = location - (255 * lower);

  // Set the lower portion of LEDs
  if(lower_brightness > 255){
    lower_brightness -= (lower_brightness - 255);
  }
  int lb = lower_brightness + spread;
  while(lb > 0 && lower >= 0){
    int factor = min(lb, 255);
    long tempcolor = color;
    int b = ((tempcolor & 255) * factor) >> 8;
    tempcolor >>= 8;
    int g = ((tempcolor & 255) * factor) >> 8;
    tempcolor >>= 8;
    int r = ((tempcolor & 255) * factor) >> 8;
    //int r = min(lb, 255);
    //int g = r;
    //int b = r;

    // Check if there were colors set previously, and mix (average)
    unsigned long prevColor = pixels->getPixelColor(lower);
    if(prevColor > 0){
      b += (prevColor & 255);
      b /= 2;
      prevColor >>= 4;
      g += (prevColor & 255);
      g /= 2;
      prevColor >>= 4;
      r =  (prevColor & 255);
      r /= 2;
    }
    pixels->setPixelColor(lower, pixels->Color(r, g, b));
    lb -= 255;
    lower--;
  }

  if(upper_brightness > 255){
    upper_brightness -= (upper_brightness - 255);
  }
  int ub = upper_brightness + spread;
  while(ub > 0 && upper < totalPixels){
    int factor = min(ub, 255);
    long tempcolor = color;
    int b = ((tempcolor & 255) * factor) >> 8;
    tempcolor >>= 8;
    int g = ((tempcolor & 255) * factor) >> 8;
    tempcolor >>= 8;
    int r = ((tempcolor & 255) * factor) >> 8;

    // Check if there were colors set previously, and mix (average)
    unsigned long prevColor = pixels->getPixelColor(upper);
    if(prevColor > 0){
      b += (prevColor & 255);
      b /= 2;
      prevColor >>= 4;
      g += (prevColor & 255);
      g /= 2;
      prevColor >>= 4;
      r =  (prevColor & 255);
      r /= 2;
    }
    pixels->setPixelColor(upper, pixels->Color(r, g, b));
    ub -= 255;
    upper++;
  }

  pixels->show();
}

void highlight(JsonArray locations, JsonArray colors){
  if(colors){
  //TODO: Replace this with a .begin() iterator for both
    for(int i = 0; i < locations.size(); i++){
      do_highlight(bottleLocations[locations[i].as<int>()], colors[i].as<long>(), 255);
    }
  } else {
    for(int i = 0; i < locations.size(); i++){
      do_highlight(bottleLocations[locations[i].as<int>()], 0xffffff, 255);
    }
  }
}

void setup() {
  Serial.begin(19200);
  pixels = new Adafruit_NeoPixel(totalPixels, pin, pixelFormat);
  pixels->begin();
  pixels->setBrightness(255);
  flow = 0;
}

void loop() {
  if(Serial.available()){
    String message = "";
    while(Serial.available()) {message = Serial.readStringUntil(0);}

    deserializeJson(doc, message);

    const char* cmd = doc["command"];
    if(strcmp(cmd, "highlight") == 0){
      flow = -1;
      pixels->clear();
      JsonArray locations = doc["locations"].as<JsonArray>();
      JsonArray colors  = doc["colors"].as<JsonArray>();
      highlight(locations, colors);
    } else if(strcmp(cmd, "idle") == 0){
      flow = 0;
      flowDirection = 1;
      //pixels->clear();
    } else {
      flow = -1;
      Serial.print("No matching command for: ");
      Serial.println(cmd);
    }
  } else if(flow >= 0){
    pixels->clear();
    int increment = 10;
    do_highlight(flow, 0xffffff, 255);
    flow += (flowDirection * increment);
    if(flow + (increment * flowDirection) <= 0 || flow + (increment * flowDirection) >= totalLocations){
      flowDirection *= -1;
    }
    delay(20);
  }
}