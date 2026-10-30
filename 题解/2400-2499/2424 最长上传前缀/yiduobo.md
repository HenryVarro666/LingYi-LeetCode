---
title: "2424. 最长上传前缀"
aliases: ["yiduobo的每日leetcode 2424.最长上传前缀"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/design", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/582034950"
zhihu_id: "582034950"
zhihu_title: "yiduobo的每日leetcode 2424.最长上传前缀"
question_id: "2424"
question: "最长上传前缀"
problem_url: "https://leetcode.cn/problems/longest-uploaded-prefix/"
difficulty: "Medium"
created: "2022-11-10T01:11:39+08:00"
updated: "2022-11-10T01:11:39+08:00"
upvotes: 0
comments: 0
---

# 2424. 最长上传前缀

> **[yiduobo的每日leetcode 2424.最长上传前缀](https://zhuanlan.zhihu.com/p/582034950) · 知乎 · 2022-11-10 · 赞同 0**
> 力扣：[2424. 最长上传前缀](https://leetcode.cn/problems/longest-uploaded-prefix/) · Medium · 灵茶山艾府：[利用最长上传前缀不会减小的性质](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2424.最长上传前缀

[力扣](https://leetcode.cn/problems/longest-uploaded-prefix/)

题目看似是一个区间问题，但是有一点可以明确的是，对着上传的进行，题目要查询的当前最长上传前缀必然是越来越长的。因此只需记录所有已上传的部分，当每次询问时，在上次询问结果的基础上继续向后查询当前的最长上传前缀即可，这个查询过程均摊下来是O(1)的。

最后附上python代码：

```python
class LUPrefix(object):

    def __init__(self, n):
        """
        :type n: int
        """
        self.p = 0
        self.n = n
        self.uploaded = [False] * n

    def upload(self, video):
        """
        :type video: int
        :rtype: None
        """
        self.uploaded[video - 1] = True

    def longest(self):
        """
        :rtype: int
        """
        while self.p < self.n and self.uploaded[self.p]:
            self.p += 1

        return self.p

# Your LUPrefix object will be instantiated and called as such:
# obj = LUPrefix(n)
# obj.upload(video)
# param_2 = obj.longest()
```
