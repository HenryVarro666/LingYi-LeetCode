---
title: "744. 寻找比目标字母大的最小字母"
aliases: ["yiduobo的每日leetcode 744.寻找比目标字母大的最小字母"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/一-二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/337214825"
zhihu_id: "337214825"
zhihu_title: "yiduobo的每日leetcode 744.寻找比目标字母大的最小字母"
question_id: "744"
question: "寻找比目标字母大的最小字母"
problem_url: "https://leetcode.cn/problems/find-smallest-letter-greater-than-target/"
difficulty: "Easy"
created: "2020-12-15T23:28:52+08:00"
updated: "2020-12-15T23:28:52+08:00"
upvotes: 0
comments: 0
---

# 744. 寻找比目标字母大的最小字母

> **[yiduobo的每日leetcode 744.寻找比目标字母大的最小字母](https://zhuanlan.zhihu.com/p/337214825) · 知乎 · 2020-12-15 · 赞同 0**
> 力扣：[744. 寻找比目标字母大的最小字母](https://leetcode.cn/problems/find-smallest-letter-greater-than-target/) · Easy · 灵茶山艾府：[【模板】二分查找（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

744.寻找比目标字母大的最小字母

[力扣](https://leetcode-cn.com/problems/find-smallest-letter-greater-than-target/)

由于题目保证letters的长度不超过10000，因此直接一趟扫描判断是最简洁的方法。不过注意到题目保证letters是有序的，那么也可以运用二分查找来解决问题，性能方面会相对好一些。

最后附上python代码：

```python
class Solution(object):
    def nextGreatestLetter(self, letters, target):
        """
        :type letters: List[str]
        :type target: str
        :rtype: str
        """

        if target >= letters[-1]:
            return letters[0]
        
        l = 0
        r = len(letters)

        while l < r:
            mid = (l + r) >> 1
            if letters[mid] <= target:
                l = mid + 1
            else:
                r = mid
            
        return letters[l]
```
