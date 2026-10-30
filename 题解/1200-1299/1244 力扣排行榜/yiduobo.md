---
title: "1244. 力扣排行榜"
aliases: ["yiduobo的每日leetcode 1244.力扣排行榜"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/614322336"
zhihu_id: "614322336"
zhihu_title: "yiduobo的每日leetcode 1244.力扣排行榜"
question_id: "1244"
question: "力扣排行榜"
problem_url: "https://leetcode.cn/problems/design-a-leaderboard/"
created: "2023-03-15T23:03:44+08:00"
updated: "2023-03-15T23:03:44+08:00"
upvotes: 0
comments: 0
---

# 1244. 力扣排行榜

> **[yiduobo的每日leetcode 1244.力扣排行榜](https://zhuanlan.zhihu.com/p/614322336) · 知乎 · 2023-03-15 · 赞同 0**
> 力扣：[1244. 力扣排行榜](https://leetcode.cn/problems/design-a-leaderboard/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1244.力扣排行榜

[力扣](https://leetcode.cn/problems/design-a-leaderboard/)

涉及到数据的增、删、改、查，以及top k的求解，王道做法自然是平衡树。注意到本题score的取值范围在1到100之间，且最多只会进行1000次操作，因此score不会超过100000，那么在这里使用线段树来维护每种分数出现的次数也是可行的。

对于增删操作，可以按照常规的线段树操作来进行，不过需要额外维护一个id到score的哈希表。

对于修改操作，则可以分离成删除操作和新增操作。

对于top K之和的求解，则可以对线段树中的每棵子树都维护一个树中节点数以及树中权重和，通过节点数与K的大小关系找出数中第K大的数是多少，在这个过程中通过权重和来完成top K之和的求解。

最后附上python代码：

```python
class Leaderboard(object):

    def __init__(self):
        self.w = [0] * 262144
        self.s = [0] * 262144
        self.score_dict = {}

    def update(self, v, delta):
        now = 0
        left, right = 0, 131071
        while left != right:
            self.w[now] += delta
            self.s[now] += v * delta
            mid = (left + right) / 2
            if v <= mid:
                right = mid
                now = now + now + 1
            else:
                left = mid + 1
                now = now + now + 2
        
        self.w[now] += delta
        self.s[now] += v * delta

    def addScore(self, playerId, score):
        """
        :type playerId: int
        :type score: int
        :rtype: None
        """
        if playerId in self.score_dict:
            score += self.score_dict[playerId]
            self.update(self.score_dict[playerId], -1)
        
        self.score_dict[playerId] = score
        self.update(score, 1)

    def top(self, K):
        """
        :type K: int
        :rtype: int
        """
        now = 0
        res = 0
        left = 0
        right = 131071
        while self.w[now] != K and left != right:
            if self.w[now + now + 2] < K:
                K -= self.w[now + now + 2]
                res += self.s[now + now + 2]
                now = now + now + 1
                right = (left + right) / 2
            else:
                now = now + now + 2
                left = (left + right) / 2 + 1
        
        if left == right:
            return res + left * K
        return res + self.s[now]

    def reset(self, playerId):
        """
        :type playerId: int
        :rtype: None
        """
        
        self.update(self.score_dict[playerId], -1)
        self.score_dict.pop(playerId)

# Your Leaderboard object will be instantiated and called as such:
# obj = Leaderboard()
# obj.addScore(playerId,score)
# param_2 = obj.top(K)
# obj.reset(playerId)
```
