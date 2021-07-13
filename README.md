# Analysing Usability, User Experience, and Perceived Health Impacts related to Quality of Life based on Users' Opinion Mining
Project developed by Renato Santos in the context of the Master Degree in Informatics Engineering, DEI-FCTUC, dissertation titled "Analysing Usability, User Experience, and Perceived Health Impacts related to Quality of Life based on Users' Opinion Mining", under the supervision of Paula Alexandra Silva and Joel Perdiz Arrais.

# Abstract
With the growth of social media and the spread of the Internet, the user’s opinion become accessible in public forums. It became then possible to analyse and extract knowledge based on the textual data published by users, through the application of Natural Language Processing and Text Mining techniques. In this dissertation, these techniques are used to, based on comments posted by users on YouTube, extract information about Usability, User Experience (UX), and Perceived Health Impacts related to Quality of Life (H-QoL). This analysis focus on videos about the Just Dance series, one of the most popular interactive dance video games.

Just Dance belongs in a category of games whose purpose goes beyond entertainment - serious games - among which there is a specific type of games, exergames, which aim is to promote physical activity. Despite their positive influence on the health of their users, these often stop playing after a short period of time, leading to the loss of benefits in the medium and long term. It is in this context that the need to better understand the experience and opinions of players arises, especially how they feel and how they like to interact, so that the knowledge generated can be used to redesign games, so that these can increasingly address the preferences of end-users.

It is with this purpose, that in a serious game it is necessary to assure not only the fundamental characteristics of the functioning system, but also to provide the best possible experience and, at the same time, to understand if these positively impact players’ lives. In this way, this dissertation analyses three dimensions, observing, besides Usability and UX aspects, also H-QoL, in the corpus extrated for this dissertaion.

To meet the objectives of this dissertation, a tool was developed that extracts information from user comments on YouTube, a social media network that despite being one of the most popular, still has been little explored as a source for opinion mining. To extract information about Usability, UX and H-QoL, a pre-established vocabulary was used with an approach based on the lexicon of the English idiom and its semantic relations. In this way, the presence of 38 concepts (five of Usability, 18 of UX, and 15 of H-QoL) was annotated, and the sentiment of each comment was also analysed. Given the lack of a vocabulary that allowed for the analysis of the dimension related to H-QoL, the concepts identified in the World Health Organization’s WHOQOL-100 questionnaire were validated for user opinion mining purposes with ten specialists in the Health and Quality of Life domains.

The results of the information extration are displayed in a public dashboard that allows visitors to explore and analyse the existing data. Until the moment of this dissertation, 543 405 comments were collected from 32 158 videos, in which about 52% contain information related to the three dimensions. The performance of this annotation process, as measured through human validation with eight collaborators, obtained an general efficacy of 85%.

# Keywords
Natural Language Processing, Opinion Mining, Social Media, Text Mining, Usability, User Experience, Health, Quality of life, Just Dance


# Setting up

- Install requirements
- Create a file named "db_credentials.ini" with the credentials to your database
- Create a file named "dev_keys.txt" with the YouTube Data API Keys that you have

# Run System

- You can extract from 1:00 AM to 5:00 AM, typing:

	> sh runSystem.sh

- Or you can run thought YouTube_Extractor.py, given some inputs:
	- Initial data to extract,
	- The range of days you should search,
	- The seconds of sleep after finishing the first full iteration,
	- If you want to update the comments of videos already extracted
	- The name of the edition to search or just type 'random'
	- The local start time to start extracting
	- The final local time to suspend the extraction system


	- Following this format:

	> python3 YouTube_Extractor.py <Begin Date: YYYY-MM-DD> <Number of jump days> <timeToCheckAgain(seconds)> <check new comments> <search Game> <beginHour> <EndHour>

	- For Examples:

	> python3 YouTube_Extractor.py 2009-09-17 4300 3600 True 'random' 1 5

	> python3 YouTube_Extractor.py 2009-09-17 7 10 True 'just dance 2021' 1 5

	> python3 YouTube_Extractor.py 2019-01-01 365 2 False 'just dance now' 1 23

# Example Annotation
- Original Comment: ``` OMG I can't believe thatt the best songs on Just Dance are from french singers........... France is the best country! I loveeeee this game!!! 😍
Thanks to this,  	i started to play EVERYDAY with my friends @michel @raquel, burning lots of calories and at the same time  I have a lot of fun while i am dancing. 😀 It changed my sedentary life and helped with my behavioral abnormalities!!! #JUSTDANCE +https://www.myblog.org
```

# Public Dashboard
![Alt text](dashboard-screenshot.png?raw=true "Just Dance Dashboard")

- Watch a demo on: https://www.youtube.com/watch?v=biOp4Oyf1ic
- There are two dashboards:
	- Usability (U), User Experience (UX), and Perceived Health-Related Quality of Life (H-QoL) Impacts
	- YouTube Analytics
- Visit on https://bit.ly/dashboard-just-dance

# Check more 
Check more about this project: https://linktr.ee/justdanceproject

# Contact
If you have any questions or suggestions, please e-mail us on renatojms@student.dei.uc.pt


