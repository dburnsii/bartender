xset s 0 && xset -dpms
firefox --kiosk --window-size=800,480 --private-window http://localhost:3000
WINDOW_ID=$(xdotool search --onlyvisible --name firefox)
xdotool windowsize $WINDOW_ID 800 480
