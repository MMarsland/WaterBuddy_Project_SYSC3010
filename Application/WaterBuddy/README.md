# Water Buddy Smart App

## Description
Android based application for monitoring and adjusting realtime firebase data. This application allows user creation, and water station monitoring by creating a GUI for the system Firebase Database. Unit tests can be performed using the Android Studio IDE.

### WaterBuddy Smart Phone application instructions
The WaterBuddy application can be installed by using the pre-built [apk](build/water_buddy.apk). Alternatively the application can be built inside Android Studio by downloading and opening this project.

Once launched there is an option in the application to either log in to a current account or create a new user account. If you are a first time user then type in your desired username and password and select the "create new account" option.

After logging into your account you can edit your user settings such as height, weight, and thirst level by selecting the gear button in the top right of the application. This is also where a user can add friends to their account.

Stations can be registered by selecting the "register station" button and then entering your WaterBuddy stations id. The user can register as many stations as they own and can change their view by selecting the blue button on the top left of the application. The application connects to the firebase database and displays all relevant information about the selected WaterBuddy station, including current humidity, daily/weekly water intake, and the water frequency of the station. Once a station is registered you should see a view similar to the one below:

<p align="center">
  <img src="../../Images/application_main_view.jpg" width="200" height="300">
</p>

The cup size of your station can be edited in the "Cup Size" section and selecting "confirm". Editing this value will change how much water your WaterBuddy station dispenses so be careful to use the correct amount.


## Unit Test
Unit Test Demo file for account creation and firebase communication can be found [here](app/src/androidTest/java/com/application/waterbuddy/UnitTest.java)

## IDE Version info
Java based Android application with the following Android Studio version

*Android Studio Bumblebee | 2021.1.1 Patch 1
Build #AI-211.7628.21.2111.8139111, built on February 1, 2022
Runtime version: 11.0.11+0-b60-7590822 amd64
VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
Linux 5.4.0-97-generic
GC: G1 Young Generation, G1 Old Generation
Memory: 1280M
Cores: 12
Registry: external.system.auto.import.disabled=true
Non-Bundled Plugins: Dart (211.7798), io.flutter (64.0.2)
Current Desktop: ubuntu:GNOME*
