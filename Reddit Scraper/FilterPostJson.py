#Combining redditPost and filterPostJson with a new file meant to scrape reddit subreddit can
#allow for an automatic scraper
import json
import csv

#Path of the json file with the post and comments. Should be postData.json
with open("C:\\Users\\Jonsi\\OneDrive\\Desktop\\Projects\\Python\\Personal Projects\\Automate\\postData.json", "r", encoding='utf-8') as file:
    data = json.load(file)

countOfComments = 0
countOfAnonymous = 242 #Number of anonymous comments so far. Reset to zero if starting over
listOfRegisterdNames = []
listContainingDict = []
listOfPost = []
postDict = {'author': 'Anonymous', 'subreddit': 'sub', 'postLink': 'url', 'commentCount': 0,'upvoteCount': 0}
postDict['author'] = data['info']['author']
postDict['subreddit'] = data['info']['subreddit']
postDict['postLink'] = data['info']['postLink']
#postDict['commentCount'] = data['info']['commentCount'] This is not the amount of scraped comments
postDict['upvoteCount'] = data['info']['upvoteCount']


#find the dislikes, upvotes, and downvotes of each comment in a post
for i in data['comments']:
    mainCommentDict = {'author': 'Anonymous', 'commentBody': 'comment', 'upvotes': 0, 'downvotes': 0, 'dislikes': 0}
    countOfComments = countOfComments + 1
    if i['author']:
        listOfRegisterdNames.append(i['author'])
        mainCommentDict['author'] = i['author']
        mainCommentDict['commentBody'] = i['commentBody']
        mainCommentDict['upvotes'] = i['upvotes']
        mainCommentDict['downvotes'] = i['downvotes']
        mainCommentDict['dislikes'] = i['dislikes']
        listContainingDict.append(mainCommentDict)
        '''print("Name: " + i['author'] + " Upvotes: " + 
              str(i['upvotes']) + " Downvotes: " + str(i['downvotes']) + " Dislikes: " + str(i['dislikes']))'''
    else:
        countOfAnonymous = countOfAnonymous + 1
        mainCommentDict['author'] = "Anonymous" + str(countOfAnonymous)
        mainCommentDict['commentBody'] = i['commentBody']
        mainCommentDict['upvotes'] = i['upvotes']
        mainCommentDict['downvotes'] = i['downvotes']
        mainCommentDict['dislikes'] = i['dislikes']
        listContainingDict.append(mainCommentDict)
        '''print("Anonymous" + " Upvotes: " + 
              str(i['upvotes']) + " Downvotes: " + str(i['downvotes']) + " Dislikes: " + str(i['dislikes']))'''
    try:
        if i['replies']:
            for j in i['replies']:
                countOfComments = countOfComments + 1
                replyComDict = {}
                if j['author']:
                    replyComDict['author'] = j['author']
                    replyComDict['commentBody'] = j['commentBody']
                    replyComDict['upvotes'] = j['upvotes']
                    replyComDict['downvotes'] = j['downvotes']
                    replyComDict['dislikes'] = j['dislikes']
                    listOfRegisterdNames.append(j['author'])
                    listContainingDict.append(replyComDict)
                    '''print("Name: " + j['author'] + " Upvotes: " + 
                            str(j['upvotes']) + " Downvotes: " + str(j['downvotes']) + " Dislikes: " + str(j['dislikes']))'''
                else:
                    countOfAnonymous = countOfAnonymous + 1
                    replyComDict['author'] = "Anonymous" + str(countOfAnonymous)
                    replyComDict['commentBody'] = j['commentBody']
                    replyComDict['upvotes'] = j['upvotes']
                    replyComDict['downvotes'] = j['downvotes']
                    replyComDict['dislikes'] = j['dislikes']
                    listContainingDict.append(replyComDict)
                    '''print("Anonymous" + " Upvotes: " + 
                            str(j['upvotes']) + " Downvotes: " + str(j['downvotes']) + " Dislikes: " + str(j['dislikes']))'''
    except:
        pass

uniqueNames = set(listOfRegisterdNames)
print(countOfComments)
print(countOfAnonymous)
#print(listContainingDictOfComments)

#Append to the comment CSV file
with open('postComments.csv', 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['author', 'commentBody','upvotes', 'downvotes', 'dislikes']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #writer.writeheader()
    writer.writerows(listContainingDict)


postDict['commentCount'] = countOfComments #Actual count of comments scraped
listOfPost.append(postDict)

#Append to the Post CSV File
with open('post.csv', 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['author', 'subreddit', 'postLink', 'commentCount','upvoteCount']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerows(listOfPost)
