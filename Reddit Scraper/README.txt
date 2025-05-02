To run the following programs you will need:
-Python installed
-httpx installed 
-parsel installed

How each program operates:

"redditPostScaper.py":
- For this program to work, it is necessary to have the link of the post that should be scraped.
  The link should not be refrencing old reddit since this may cause an error. 
- This program initialize an async httpx client that will act like a basic browser.
- After successfully receiving a response, the scraper will scrape the post provided by the link
- In this program, it possible to get data about the author of the post, comment count of the post,
  upvotes of the post, the subreddit and more.
- After scraping the post, it will then try to scrape the comments of the post by using the old
  reddit link version of the provided link. 
- For the sake of this project, the limit of how many comments that can be scraped at one time is 500.
  It is also possible to scrape less or more.
- The results of the sucessful scraped will then be stored in "postData.json". It not necessary to create
  this file since it should be automatically created when this program is runned. However, this program
  only supports one post per run currently and will not append to the postData.json. Therefore it is necessary
  to run "FilterPostJson.py" right after it.

"FilterPostJson.py" :
- This program requires the use of "postData.json" to create "postComments.csv" and "post.csv"
- This program must be runned after "redditPostScaper.py" to not lose any potential data. 
- This programs works by first gathering the author, post link, upvote count, and subreddit of the
  post. Then it would loop though the comments of "postData.json" to gather the comments of that post.
- This programs gather the following infomation:
    - How many anonymous comments and comment count of stored data. 
    - Author, post link, upvote count, and subreddit of the post
    - Author, comment, upvotes, downvotes, dislikes of the comment
- This infomraiton is stored in "postComments.csv", which holds the data of the comments, and "post.csv",
  which holds the data of the post.


*NOTE* The actual analysis of the data was done in excel. The collect information is stored in "redditScrapedExcel.xlsx".




