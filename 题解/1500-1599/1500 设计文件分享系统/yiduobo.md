---
title: "1500. 设计文件分享系统"
aliases: ["yiduobo的每日leetcode 1500.设计文件分享系统"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/617038881"
zhihu_id: "617038881"
zhihu_title: "yiduobo的每日leetcode 1500.设计文件分享系统"
question_id: "1500"
question: "设计文件分享系统"
problem_url: "https://leetcode.cn/problems/design-a-file-sharing-system/"
created: "2023-03-26T00:01:30+08:00"
updated: "2023-03-26T00:01:30+08:00"
upvotes: 0
comments: 0
---

# 1500. 设计文件分享系统

> **[yiduobo的每日leetcode 1500.设计文件分享系统](https://zhuanlan.zhihu.com/p/617038881) · 知乎 · 2023-03-26 · 赞同 0**
> 力扣：[1500. 设计文件分享系统](https://leetcode.cn/problems/design-a-file-sharing-system/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1500.设计文件分享系统

[力扣](https://leetcode.cn/problems/design-a-file-sharing-system/)

首先，题目中每个用户所拥有的文件以及每个文件的拥有者都需要记录下来，因此需要使用两个哈希数组记录来记录这些信息。另一方面，在join操作时需要得到当前未使用的最小的id，因此还需要一个堆来记录由于leave操作空闲下来的id，以及一个变量用来记录下一个从未使用过的最小id。

接下来，对于题目中要求的操作：

1、join操作：

首先需要想办法找出当前最小的未使用的用户id，那么当记录空闲id的堆不为空时，就应该取堆顶的id作为这个新用户的id，否则就需要使用下一个从未使用过的最小id作为该用户的id。

确定了id后，则需要更新上面所说的两个哈希表。

2、leave操作：

首先需要从该用户所拥有的所有文件的拥有者哈希表中将当前用户剔除，然后将当前用户从拥有文件哈希表中剔除，然后将当前用户的id加入到空闲id的堆中。

3、request操作：

根据用户id从哈希表中取出文件列表，排序后即为所求。若这个列表非空，还需要分别更新当前用户所拥有的文件以及该文件的拥有者。

最后附上python代码：

```python
class FileSharing(object):

    def __init__(self, m):
        """
        :type m: int
        """
        self.chunk_owner = [set() for _ in range(m + 1)]
        self.owned_chunk = {}
        self.idle_id = []
        self.next_id = 1

    def join(self, ownedChunks):
        """
        :type ownedChunks: List[int]
        :rtype: int
        """
        if self.idle_id:
            id = heapq.heappop(self.idle_id)
        else:
            id = self.next_id
            self.next_id += 1
        
        self.owned_chunk[id] = set(ownedChunks)
        for chunk in ownedChunks:
            self.chunk_owner[chunk].add(id)
        
        return id

    def leave(self, userID):
        """
        :type userID: int
        :rtype: None
        """
        heapq.heappush(self.idle_id, userID)
        for chunk in self.owned_chunk[userID]:
            self.chunk_owner[chunk].remove(userID)
        self.owned_chunk.pop(userID)

    def request(self, userID, chunkID):
        """
        :type userID: int
        :type chunkID: int
        :rtype: List[int]
        """
        res = sorted(list(self.chunk_owner[chunkID]))
        
        if res:
            self.chunk_owner[chunkID].add(userID)
            self.owned_chunk[userID].add(chunkID)
        return res

# Your FileSharing object will be instantiated and called as such:
# obj = FileSharing(m)
# param_1 = obj.join(ownedChunks)
# obj.leave(userID)
# param_3 = obj.request(userID,chunkID)
```
