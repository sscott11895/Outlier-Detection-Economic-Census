# On the Outs: Rethinking Outlier Detection in the Economic Census


In the summer of 2022, I interned with with the Data Science team at the U.S. Census Bureau
Economy-Wide Statistics Division. I was placed with this team through the [Civic Digital Fellowship at Coding it Forward](https://www.codingitforward.com/about),
an organization that places early-career data analysts, data scientists, and product managers with federal 
government agencies to support innovation and design. My work was focused on researching 
and creating a proof of concept of an outlier identification tool in the 
form of a Tableau dashboard. 








My work this summer has served as the basis of a new outlier review process and aims to 
support over 150 analysts in correcting data from the 2022 Economic Census in preparation for the 
Geographic Area Series publication. 





My specific focus was 


My 
The Civic Digital Fellowship is empowering the next generation of technology leaders to innovate at the intersections of technology and public service in federal government offices across the United States. Fellows work across software engineering, data, design, and product management to deliver policy, improve systems, and strengthen products on behalf of the American people.





tives. 
One popular, and at times controversial, initiative was the introduction of e-scooters
in various neighborhoods around Chicago. While this new mode of transportation offers 
commuters and tourists an alternative to gas-powered vehicles, concerns around sidewalk
clutter are often sources of debate. 


Chicago piloted an E-Scooter program in 2020 to test how city residents would
respond to this new mode of transportation. The city’s full report can be found [here](https://www.chicago.gov/content/dam/city/depts/cdot/Misc/EScooters/2021/2020%20Chicago%20E-scooter%20Evaluation%20-%20Final.pdf).

The goal of my analysis is to look at the origin and end points of scooter rides.
Where were these novel wheels popular and where did they sit growing dust and 
rust on the sidewalk? I am using the raw data provided on the City of Chicago website, 
which can be found [here](https://data.cityofchicago.org/Transportation/E-Scooter-Trips-2020/3rse-fbp6).


# Contents

The R Markdown is included in this repo with various plots and maps that supported 
my analysis (see here for full report). During the data manipulation and processing phase, I used geolocation data 
to review trip duration, trip distance, origin communities, and destination communities.  

I then used a brief time-series analysis to see the number of trips taken over time. 
From mid-August to early September, we can see that residents quickly learned 
of the program and began utilizing the scooters. The number of rides generally 
decreases over time which is congruent with the expected drop in temperatures as 
the weather changes throughout the fall.

Finally, I used maps to visualize communities where e-scooters were very popular based on 
ridership. After looking at this data, it is clear that scooters were well utilized
in neighborhoods in the north of Chicago. While more data is needed to understand why 
people in southern neighborhoods might not choose to travel by bike, one conjecture we 
could make is that people in northern Chicago might live and work within a two block radius. 
In contrast, people in southern Chicago might travel farther to get to work and therefore 
traveling by scooter is a less attractive option.
