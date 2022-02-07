# KNOWN BUGS: If the date week rolls over a month it will simply add 6 without rolling. In "({weekStartDate.strftime("%B")} {weekStartDate.day}-{weekStartDate.day+6})"
# What week is week 1? IT says starting with week 3? When is that?

import os
import datetime

students = ["Michael Marsland"] # Put your name here

dates = [datetime.date(2022, 1, 24)]
for i in range(1,11):
    dates.append(dates[-1] + datetime.timedelta(days=7))

for weekNum, weekStartDate in enumerate(dates):
    if (datetime.date.today() > weekStartDate):
        weekDir = f"Week{weekNum+3}"
        if not os.path.exists(weekDir):
            os.mkdir(weekDir)
        for studentName in students:
            [firstName, lastName] = studentName.split()
            filename = f"Week{weekNum+3}/{firstName}_{lastName}_week{weekNum+3}.md"
            if not os.path.exists(filename):
                f = open(filename, "w+")

                f.write(f"""## Weekly Individual Project Update Report
### Group number: L3_G7
### Student name: {firstName} {lastName}
### Week: Week {weekNum+3} ({weekStartDate.strftime("%B")} {weekStartDate.day}-{weekStartDate.day+6})  

1. ***How many hours did you spend on the project this week? (0-10)***
   
2. ***Give rough breakdown of hours spent on 1-3 of the following:***
(meetings, information gathering, design, research, brainstorming, evaluating options, prototyping options, writing/documenting, refactoring, testing, software implementation, hardware implementation)
   1. Top item: activity, hours
   2. 2nd item: activity, hours
3. ***What did you accomplish this week?***
   - 
- 
4. ***How do you feel about your progress?***
   - 
5. ***What are you planning to do next week***?
   - 
   - 
6. ***Is anything blocking you that you need from others?***
   -
""")
                f.close()