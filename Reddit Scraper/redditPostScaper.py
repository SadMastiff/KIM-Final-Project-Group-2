#Combining redditPost and filterPostJson with a new file meant to scrape reddit subreddit can
#allow for an automatic scraper
import json
import asyncio
from typing import List, Dict, Union
from httpx import AsyncClient, Response
from parsel import Selector
from loguru import logger as log

# initialize an async httpx client
client = AsyncClient(
    # enable http2
    http2=True,
    # add basic browser like headers to prevent getting blocked
    headers={
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": "intl_splash=false"
    },
    follow_redirects=True
)

def parse_post_info(response: Response) -> Dict:
    #parse post data from a subreddit post
    #Anything that could have been useful
    selector = Selector(response.text)
    info = {}
    label = selector.xpath("//faceplate-tracker[@source='post']/a/span/div/text()").get()
    comments = selector.xpath("//shreddit-post/@comment-count").get()
    upvotes = selector.xpath("//shreddit-post/@score").get()
    info["authorId"] = selector.xpath("//shreddit-post/@author-id").get()
    info["author"] = selector.xpath("//shreddit-post/@author").get()
    info["authorProfile"] = "https://www.reddit.com/user/" + info["author"] if info["author"] else None
    info["subreddit"] = selector.xpath("//shreddit-post/@subreddit-prefixed-name").get()
    info["postId"] = selector.xpath("//shreddit-post/@id").get()
    info["postLabel"] = label.strip() if label else None
    info["publishingDate"] = selector.xpath("//shreddit-post/@created-timestamp").get()
    info["postTitle"] = selector.xpath("//shreddit-post/@post-title").get()
    info["postLink"] = selector.xpath("//shreddit-canonical-url-updater/@value").get() #Does not work
    info["commentCount"] = int(comments) if comments else None
    info["upvoteCount"] = int(upvotes) if upvotes else None
    info["attachmentType"] = selector.xpath("//shreddit-post/@post-type").get()
    info["attachmentLink"] = selector.xpath("//shreddit-post/@content-href").get()
    return info


def parseAllCommentsOfPost(response: Response) -> List[Dict]:
    #parse post comments
    def parseAComment(parent_selector) -> Dict:
        #parse a comment object
        author = parent_selector.xpath("./@data-author").get()
        link = parent_selector.xpath("./@data-permalink").get()
        dislikes = parent_selector.xpath(".//span[contains(@class, 'dislikes')]/@title").get() #Bugged?
        upvotes = parent_selector.xpath(".//span[contains(@class, 'likes')]/@title").get() #sufficient for project
        downvotes = parent_selector.xpath(".//span[contains(@class, 'unvoted')]/@title").get()  #Bugged?     
        return {
            "authorId": parent_selector.xpath("./@data-author-fullname").get(),
            "author": author,
            "authorProfile": "https://www.reddit.com/user/" + author if author else None,
            "commentId": parent_selector.xpath("./@data-fullname").get(),
            "link": "https://www.reddit.com" + link if link else None,
            "publishingDate": parent_selector.xpath(".//time/@datetime").get(),
            "commentBody": parent_selector.xpath(".//div[@class='md']/p/text()").get(),
            "upvotes": int(upvotes) if upvotes else None,
            "dislikes": int(dislikes) if dislikes else None, #Bugged?
            "downvotes": int(downvotes) if downvotes else None, #Bugged?      
        }

    def parseReplies(what) -> List[Dict]:
        #recursively parse replies
        replies = []
        for reply_box in what.xpath(".//div[@data-type='comment']"):
            replyComment = parseAComment(reply_box)
            replyToReply = parseReplies(reply_box)
            if replyToReply:
                replyComment["replies"] = replyToReply
            replies.append(replyComment)
        return replies

    selector = Selector(response.text)
    data = []
    for i in selector.xpath("//div[@class='sitetable nestedlisting']/div[@data-type='comment']"):
        comment = parseAComment(i)
        replies = parseReplies(i)
        if replies:
            comment["replies"] = replies
        data.append(comment)            
    return data

#Sort shows up as error but works if defined when called
async def scrapePost(url: str, sort: Union["old", "new", "top"]) -> Dict:
    #crape subreddit post and comment data
    response = await client.get(url)
    
    postData = {}
    postData["info"] = parse_post_info(response)
    #Scrape the comments from the old.reddit version
    postData["info"]["postLink"] = url #There is a bug with post link not actual having the URL. Temp solution
    #Limit set to 500. Should be enough since desk treadmills are not popular
    commentPageURL = postData["info"]["postLink"].replace("www", "old") + f"?sort={sort}&limit=500"
    response = await client.get(commentPageURL)
    postData["comments"] = parseAllCommentsOfPost(response) 
    return postData

#Run the scraper by putting post link you want. Sort by either top, new, or old
async def run():
    postAndCommentData = await scrapePost(
        url="https://www.reddit.com/r/WFH/comments/199089l/my_under_desk_treadmill_journey_2024/",
        sort="top" #Ensures the comment with most upvotes get picked up
    )

    #Write to a json that holds information about one post
    with open("postData.json", "w", encoding="utf-8") as file:
        json.dump(postAndCommentData, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    asyncio.run(run())