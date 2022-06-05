# Behavior Tracker
#### TCSS-506 Spring 2022 Full Stack Project for team DNS

### Features
1) Accounts
2) Trackee management with dashboard
3) Frequency tracking over timed duration
4) Duration tracking

### How to deploy (assumes you're familiar with docker)
1) Build docker container from root directory
2) Run docker container

### How to explore application
1) Create a user account
2) Log in using newly registered account
3) At dashboard, create a new person whose behavior to track (example, as a professor, you may have a particularly disruptive student in class who likes to make jokes for attention, or you might have a child at home struggling with a particular behavior like bedwetting and want to track if it is improving or getting worse for their medical provider).
4) Add the person's pseudonym (initials, nickname, whatever), and any notes (triggered by loud noises, has rough times with change, needs extra patience due to problems at home, recently moved to new caregivers, etc), then click Add
5) Click on the person's name - you can update or delete them if you choose to.
6) Click log a behavior.
7) Enter behavior name to track (example hitting), then track related data.
   1) If tracking straight frequency (example, weekly bedwetting or incidents of stealing, enter total frequency, then save)
   2) If tracking frequency per time unit (example, interruptions in a 30 minute math lesson), click start on the time, then tally the behavior either by clicking on the up tracker as the beavior occurs in the time window (example 30 minutes is frequent), then stop when the desired time has elapsed, and then save.
   3) If tracking straight duration (example, throwing objects around the room), simply click start as the behavior starts occurring, stop when it stops, then save.
8) Be sure to click save after finishing tracking the behavior.
9) Click Dashboard to return to screen of all people at any time.
10) Click on individual people to delete or update people or notes and pseudonyms at any time.