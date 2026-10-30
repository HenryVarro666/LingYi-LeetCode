---
title: "1236. 网络爬虫"
aliases: ["yiduobo的每日leetcode 1236.网络爬虫"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/614038714"
zhihu_id: "614038714"
zhihu_title: "yiduobo的每日leetcode 1236.网络爬虫"
question_id: "1236"
question: "网络爬虫"
problem_url: "https://leetcode.cn/problems/web-crawler/"
created: "2023-03-14T23:15:36+08:00"
updated: "2023-03-14T23:15:36+08:00"
upvotes: 0
comments: 0
---

# 1236. 网络爬虫

> **[yiduobo的每日leetcode 1236.网络爬虫](https://zhuanlan.zhihu.com/p/614038714) · 知乎 · 2023-03-14 · 赞同 0**
> 力扣：[1236. 网络爬虫](https://leetcode.cn/problems/web-crawler/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1236.网络爬虫

[力扣](https://leetcode.cn/problems/web-crawler/)

bfs的问题。从startUrl开始进行爬取，对于当前爬取到的地址，若其没有被访问过，且其域名与startUrl相同，那么就将其加入到bfs队列中。bfs完成后，整个bfs队列即为最终答案。

最后附上python代码：

```python
# """
# This is HtmlParser's API interface.
# You should not implement it, or speculate about its implementation
# """
#class HtmlParser(object):
#    def getUrls(self, url):
#        """
#        :type url: str
#        :rtype List[str]
#        """

class Solution(object):
    def crawl(self, startUrl, htmlParser):
        """
        :type startUrl: str
        :type htmlParser: HtmlParser
        :rtype: List[str]
        """

        q = [startUrl]
        vis = set([startUrl])

        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for next in htmlParser.getUrls(now):
                if next not in vis and now.split('/', 3)[2] == next.split('/', 3)[2]:
                    vis.add(next)
                    q.append(next)
                    tail += 1
        
        return q
```
