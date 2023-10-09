# douban Posts to Notion

## Motivation
www.douban.com is a Chinese social networking website for sharing thoughts, status, and marking movies, books, etc. that you are interested in. Different from other applications, it mainly focus on text sharing, and there are various disscussion groups and experience posts. I personally benefit a lot from the experience posts, while recently it started rigid reviews, and baned and deleted piles of precious posts on it, so I decided to make a crawler to save the information locally (i.e. to notion)。

There has already been some tools to achieve this, e.g. \
https://www.notion.so/for-Share-26945cf67a2a407cb9f381109dd438a1 \
for exporting the movies, books, etc. you have marked.

And like \
https://github.com/lavegree/001/issues/1 \
which applies <em>GitHub Actions</em> to save the posts to github. \
I have also tried this, but one day it just didn't work for some reason; Also I intend to save the comment (esp. the ones that have most thumb-ups) since some advice is valuable as well.

## Usage
There's a very simple Gui interface by `PyQt5` acquiring the input of your target douban page and the ID of the Notion database you want to insert the page into.

You need to have a database with properties `Author` (type: `Text`) and `URL` (type: `URL`) beforehand.
![image](https://github.com/wongzingji/douban2Notion/blob/master/images/page.png)


> Note that since the Notion API does not yet support uploading files, images or other files still links to urls on the source website. 


## Todo
- [ ] Extract the second page of the comments
- [ ] Add progress bar to the Gui interface
- [ ] Automate the creation of necessary database properties
- [ ] Adjust the format: unnecessarily start a newline in some cases
- [ ] Extend to diaries, movie lists...
