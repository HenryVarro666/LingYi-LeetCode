---
title: "2766. 重新放置石块"
aliases: ["yiduobo的每日leetcode 2766.重新放置石块"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/654981362"
zhihu_id: "654981362"
zhihu_title: "yiduobo的每日leetcode 2766.重新放置石块"
question_id: "2766"
question: "重新放置石块"
problem_url: "https://leetcode.cn/problems/relocate-marbles/"
difficulty: "Medium"
created: "2023-09-08T04:10:04+08:00"
updated: "2023-09-08T04:10:04+08:00"
upvotes: 0
comments: 0
---

# 2766. 重新放置石块

> **[yiduobo的每日leetcode 2766.重新放置石块](https://zhuanlan.zhihu.com/p/654981362) · 知乎 · 2023-09-08 · 赞同 0**
> 力扣：[2766. 重新放置石块](https://leetcode.cn/problems/relocate-marbles/) · Medium · 灵茶山艾府：[哈希集合模拟（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2766.重新放置石块

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/relocate-marbles/description/)

使用集合记录当前有石块的位置，接下来对于每次移动操作，只需将moveFrom中的位置从集合中移除，然后将moveTo中的位置加入到集合中就行了。操作完成后，将集合中的位置排序返回即可。

最后附上python代码：

```python
class Solution(object):
    def relocateMarbles(self, nums, moveFrom, moveTo):
        """
        :type nums: List[int]
        :type moveFrom: List[int]
        :type moveTo: List[int]
        :rtype: List[int]
        """

        pos = set(nums)
        for f, t in zip(moveFrom, moveTo):
            pos.remove(f)
            pos.add(t)
        
        return sorted(list(pos))
```
