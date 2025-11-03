# pdga-score-scraper

Tool to grab hole-by-hole scores for PDGA tournaments

## Project Organization

Via the cookiecutter-data-science template:

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>



## Procedure

* Determine `event_id` for event of interest via its report page:  `https://www.pdga.com/tour/event/{event_id}`
* Create virtual environment with specifications in `requirements.txt`.  Create virtual environment via Makefile command `make create_environment`.



## Included datasets
* 2025 Lost Valley Open
* 2025 Hoodoo (both Pro and Am days)




## TODO
* Extract hole pars from downloaded data rather than hardcode (notebook 2.01)
* More smartly handle environment creation (check if exists)
* Create linear regression of hole scores vs player rating to see how "accurately" scores are given to differentiate players
* How to automate report creation?  Figures in correct order


## TODONE
* Export csv
* Random wait time between scrapes


## References

* Steve Wes - BRP vs. Maple Hill scoring:  https://discgolf.ultiworld.com/2016/08/04/statistical-breakdown-blue-ribbon-pines/
* Thread of how holes should score:  https://www.dgcoursereview.com/threads/how-should-one-analyze-a-holes-performance.145607/
* Chuck Kennedy course design validation:  https://www.pdga.com/course-design-validation
* Paywalled article:  https://discgolf.ultiworld.com/2021/10/01/what-makes-a-good-disc-golf-hole-a-statistical-analysis-of-the-mvp-open/
* Thesis:  https://math.montana.edu/grad_students/writing-projects/2018/EliMeyer.pdf
* Steve West thread:  https://www.dgcoursereview.com/threads/hole-and-course-performance-statistics.137896/
* DGPT data set:  https://data.scorenetwork.org/disc_sports/DGPT24.html
* https://statmando.com/
* Sex differences in disc golf:  https://pmc.ncbi.nlm.nih.gov/articles/PMC12294547/pdf/EJSC-25-e70008.pdf
* https://discgolf.com/scoring-spread-in-course-design-and-how-to-defeat-it-tonns-travels/

* https://www.pdga.com/files/discussion/archive/t-26901.html
Chuck Kennedy, allegedly:  A hole which yields > two-thirds or 70% the same score is an indicator of bad design.  (You want some variation to distinguish between the levels of the players.)
What is the Course Design group?
Perform analysis for ~50 point groups.  Maybe similar to by division.
Color level of courses?


* https://www.pdga.com/files/discussion/archive/t-26901.html
