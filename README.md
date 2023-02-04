# On the Outs: Rethinking Outlier Detection in the Economic Census


In the summer of 2022, I interned with with the Data Science team at the U.S. Census Bureau
Economy-Wide Statistics Division. I was placed with this team through the [Civic Digital Fellowship at Coding it Forward](https://www.codingitforward.com/about),
an organization that places early-career data analysts, data scientists, and product managers with federal 
government agencies to support innovation and design. My work was focused on researching 
and creating a proof of concept of an outlier identification tool in the 
form of a Tableau dashboard. See [here](https://github.com/sscott11895/Outlier-Detection-Economic-Census/blob/main/Outlier_Detection_Presentation.pdf) 
to view my final project presentation slides. 

## Background and The Problem
The Economic Census is deployed every 5 years to assess the health and wealth of U.S. economy. All U.S. businesses
are asked to fill out information on metrics such as annual payroll, number of employees, total sales and receipts, etc. 
Once these questionnaires are filled out and returned, multiple teams at Census begin the task of cleaning and analyzing the data.
When I arrived at the Census, I met with multiple trade teams, like Manufacturing and Wholesale, who shared with me their process for 
reviewing responses with the hopes of finding, correcting, and potentially removing, outliers.
I immediately noticed that while all teams had access to a preexisting outlier detection tool developed in 2010, 
nearly all teams had abandoned this tool due to negative user experiences with the interface. Furthermore, the tool led to a 
high rate of duplication, where once an analyst reviewed and corrected a particular number, the software would often 
re-highlight the same figure and prompt a second unnecessary review. As a result, all teams were using different approaches 
when performing outlier review.

## Process
Early on in the summer, I did focus groups with 5 trade teams where they demoed their tools and 
explained their existing painpoints. Their chief complaints centered around the lack of a strong visual that could
help analysts immediately pinpoint the worst-of-the-worst outliers. During this time, I also met with upper-level
management who emphasized they wanted a tool that allowed trade teams to focus on conducting sub-state reviews of outliers,
specifically county-level review. As I was developing a python script as well as a Tableau dashboard, I used a [work paper](http://www.asasrms.org/Proceedings/y2013/files/309457_82715.pdf) 
analyzing how the modified Hidiroglou-Berthelot (HB) edit has been used for outlier detection in previous Census outlier identification tools. 
Ultimately, I used the mathematics in this paper to determine outliers in my final tool. 


## Solution
The Tableau dashboard I created utilized a geographic-centered approach. When analysts opened their trade-specific Tableau file, 
they immediately saw a map of the United States with relevant North American Industry Classification System (NAICS) code filters and important ratios.
As they click through the different combinations of these inputs, U.S. states would changes color based on whether or not the underlying mathematical method (applied to the data during the preprocessing step)
determined it to be on outlier. 

![State Demo]()




See code for [functions]() used and example code of how I [cleaned the trade-specific data]() prior to loading the information into Tableau. 


At the end of my internship, I had completed an interactive Tableau dashboard that used both geographic visuals 
as well as easy-to-digest scatter plots and tables. My work this summer has served as the basis of a new outlier review process and aims to 
support over 150 analysts in correcting data from the 2022 Economic Census in preparation for the 
Geographic Area Series publication. 






