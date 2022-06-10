# Tracker Bee
#### TCSS-506 Spring 2022 Full Stack Project for team DNS
  
Website status: Online  
http://ec2-34-205-30-233.compute-1.amazonaws.com/  
  
Pivotal Tracker  
(https://www.pivotaltracker.com/n/projects/2564451)  

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
6) Click the "Add" link in the Targeted Behaviors section to define some behaviors for the person.
7) Name the behavior and provide a short description, then click submit.  You can do this for a couple behaviors if you'd like.
8) Now it's time to take some behavior data.  Click on the "Log a behavior" link.
9) Select a behavior from the dropdown menu and choose whether to record frequency or duration data.
   1) If tracking frequency (example, weekly bedwetting or incidents of stealing) enter total frequency, then click save.
   2) If tracking frequency per time unit (example, interruptions in a 30 minute math lesson), click start on the time, then tally the behavior either by clicking on the up tracker as the behavior occurs in the time window (example 30 minutes is frequent), then stop when the desired time has elapsed, and then save.
   3) If tracking straight duration (example, throwing objects around the room), simply click start as the behavior starts occurring, stop when it stops, then save.
10) Be sure to click save after finishing tracking the behavior.  You can also try hitting save without selecting a behavior or without entering data—the app won't let you.
11) Click Dashboard to return to screen of all people at any time.  
12) Click on individual people to delete or update people or notes and pseudonyms at any time.  

### Responsibilities
1) Darence: Made it beautiful, system design doc for final presentation, pre-defined behavior names, behavior frequency/duration data collection and data logging, Javascript wizardry and majesty, anything that doesn't look identical to Hong's default app settings, gold star for comprehending weird behavior tracking info with no behavior tracking background!  
   1) styles.css, base.html, person.html, dashboard.html, behavior.html, app.py, model.py  
2) Nik: Powerpoint for practice presentation, database management, error handling, behavior log UI, behavior modeling adjustments, various touchup operations, executive dysfunction strategy.
   1) app.py, model.py, person.html, add-behavior.html, behavior.html, behavior_form.py, style.css
3) Steph: This doc!  Pivotal tracker, powerpoint for final presentation, bugs, users, people CRUD, database structure, routing
   1) person_form.py, user_form.py, add-person.html, person.html, login.html, register.html, dashboard.html, app.py, model.py
