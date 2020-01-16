## Bartender Worker

Asynchronous worker script for handling I2C and GPIO communication for the bartender.

### Websocket

-  `ws://localhost:8765`

### Endpoints

-  `{"drink": (<drink_array> | null)}`  Pour drink specified by `drink_array`, or return ETA of current drink. Returns ETA of current drink if one is already pouring, regardless of arguments.
    - `drink_array` Array of `drink_entry`s containing motor addresses and pour times (in ms) for each
        - `drink_entry` Drink address along with pour time (in ms)
            - `{"address": <I2C_Address>, "time": <pour_time>}` Address should be 16-bit integer, pour time should be 16-bit integer
-  `{"led_upper": (<rgb_value> | null)}`  Set upper LEDs to specified color, or return currently set color
    - `rgb_value`  String in format "#RRGGBB"
-  `{"led_lower": (<rgb_value> | null)}`  Set lower LEDs to specified color, or return currently set color
    - `rgb_value`  String in format "#RRGGBB"
-  `{"lcd": <text>}`  Set LCD text to specified value
    - `text`  String with no more than 2 lines, with 16 characters per line. Any additional will be truncated.
    
    