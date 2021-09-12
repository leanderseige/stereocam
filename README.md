# DIY Stereo Camera

A quick Sunday project: build a quick and easy stereo camera. You get two mobile devices: VR glasses and a mobile stereo camera, connected to each other.

![Stereo Cam and Glasses](./images/sc-overview.jpg)

## Material
- a Raspberry Pi with Raspbian (I used Model 4 / 4GB plus an additional Fan)
- two cheap USB webcams
- an old box
- a Powerbank
- one of those cheap plastic VR head mount frames for your phone

Build it all together:

![Stereo Cam im Browser](./images/sc-box.jpg)

## Install necessary Software

```
sudo apt-get install python python-opencv python-flask build-essential libssl-dev
```

## Run it

Clone this repo

```
git@github.com:leanderseige/stereocam.git
```
and run the server
```
flask run --host=0.0.0.0
```
Now check with your browser and your phone's browser (should be on the same WLAN).

Carefully adjust the cameras, has great impact on how goot it works!

![Stereo Cam im Browser](./images/sc-browser.png)

Put the phone in the VR frame and enjoy!

![Stereo Cam im Browser](./images/sc-arrange.jpg)

## Run it

Todo's:
- fullscreen mode must be adjusted for Apple phones
