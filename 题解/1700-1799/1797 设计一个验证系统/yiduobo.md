---
title: "1797. 设计一个验证系统"
aliases: ["yiduobo的每日leetcode 1797.设计一个验证系统"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/463626640"
zhihu_id: "463626640"
zhihu_title: "yiduobo的每日leetcode 1797.设计一个验证系统"
question_id: "1797"
question: "设计一个验证系统"
problem_url: "https://leetcode.cn/problems/design-authentication-manager/"
created: "2022-02-02T15:53:12+08:00"
updated: "2022-02-02T15:53:12+08:00"
upvotes: 0
comments: 0
---

# 1797. 设计一个验证系统

> **[yiduobo的每日leetcode 1797.设计一个验证系统](https://zhuanlan.zhihu.com/p/463626640) · 知乎 · 2022-02-02 · 赞同 0**
> 力扣：[1797. 设计一个验证系统](https://leetcode.cn/problems/design-authentication-manager/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1797.设计一个验证系统

[力扣](https://leetcode-cn.com/problems/design-authentication-manager/)

对于这类问题，一个经典的做法就是延迟更新。具体到本题，就是某个token到期后，并不是立即处理这个token，而是等到下次访问这个token，或者统计汇总信息的时候再更新这个token的信息。

对于本题，是使用哈希表来储存每个token最新的更新时间。对于题目中的集中操作：

1、新增：以token为key加入到哈希表中，对应的value为当前时间

2、更新：若当前token在哈希表中，那么需要先根据这个token加入哈希表的时间以及当前时间判断这个token是否已经过期。若过期，那么将其从哈希表中移除，否则更新这个token对应的时间

3、统计未过期的token：遍历哈希表中的所有token，若当前token过期了，那么将其移除。遍历完成后，返回哈希表中剩余的token数目

最后附上python代码：

```python
class AuthenticationManager(object):

    def __init__(self, timeToLive):
        """
        :type timeToLive: int
        """
        self.timeToLive = timeToLive
        self.tokenDict = {}

    def generate(self, tokenId, currentTime):
        """
        :type tokenId: str
        :type currentTime: int
        :rtype: None
        """
        self.tokenDict[tokenId] = currentTime

    def renew(self, tokenId, currentTime):
        """
        :type tokenId: str
        :type currentTime: int
        :rtype: None
        """
        if tokenId in self.tokenDict:
            if currentTime - self.tokenDict[tokenId] >= self.timeToLive:
                self.tokenDict.pop(tokenId)
            else:
                self.tokenDict[tokenId] = currentTime

    def countUnexpiredTokens(self, currentTime):
        """
        :type currentTime: int
        :rtype: int
        """
        res = 0
        for tokenId in self.tokenDict.keys():
            if currentTime - self.tokenDict[tokenId] >= self.timeToLive:
                self.tokenDict.pop(tokenId)
            else:
                res += 1
        
        return res

# Your AuthenticationManager object will be instantiated and called as such:
# obj = AuthenticationManager(timeToLive)
# obj.generate(tokenId,currentTime)
# obj.renew(tokenId,currentTime)
# param_3 = obj.countUnexpiredTokens(currentTime)
```
