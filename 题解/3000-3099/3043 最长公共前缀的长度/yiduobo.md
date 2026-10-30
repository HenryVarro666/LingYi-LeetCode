---
title: "3043. 最长公共前缀的长度"
aliases: ["yiduobo的每日leetcode 3043.最长公共前缀的长度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "题单/常用数据结构", "题单/常用数据结构/六-字典树-trie"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/696047596"
zhihu_id: "696047596"
zhihu_title: "yiduobo的每日leetcode 3043.最长公共前缀的长度"
question_id: "3043"
question: "最长公共前缀的长度"
problem_url: "https://leetcode.cn/problems/find-the-length-of-the-longest-common-prefix/"
difficulty: "Medium"
created: "2024-05-05T22:12:05+08:00"
updated: "2024-05-05T22:12:05+08:00"
upvotes: 1
comments: 0
---

# 3043. 最长公共前缀的长度

> **[yiduobo的每日leetcode 3043.最长公共前缀的长度](https://zhuanlan.zhihu.com/p/696047596) · 知乎 · 2024-05-05 · 赞同 1**
> 力扣：[3043. 最长公共前缀的长度](https://leetcode.cn/problems/find-the-length-of-the-longest-common-prefix/) · Medium · 灵茶山艾府：[两种写法：用字符串/不用字符串（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3043.最长公共前缀的长度

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-length-of-the-longest-common-prefix/description/)

题目保证了数组内的数值大小在10^8以内，也就是说每个数字最多只有9个前缀，同时每种前缀都在整数的取值范围内。另一方面，由于数组的长度不超过50000，因此即使不考虑重复的情况，每个数组中的数也最多只有450000种前缀，完全可以全部计算出来。分别计算出来后，就可以通过集合判断arr2的前缀是否在arr1中的前缀中出现过。

于是可以先对arr1进行一趟遍历，利用集合统计每种前缀，接下来再对arr2进行一趟遍历，检测当前前缀是否出现在集合中，若出现过，那么取位数最多的作为最终答案。

具体实现上，可以通过不断地除10操作来获取所有的前缀，另外数值最大的前缀必然是最长的前缀，因此在寻找位数最多的前缀时可以直接选数值最大的前缀，最后再计算其位数作为结果返回。

最后附上python代码：

```python
class Solution(object):
    def longestCommonPrefix(self, arr1, arr2):
        """
        :type arr1: List[int]
        :type arr2: List[int]
        :rtype: int
        """

        prefix = set()
        for v in arr1:
            while v:
                prefix.add(v)
                v /= 10
        
        ma = 0
        for v in arr2:
            while v:
                if v in prefix:
                    ma = max(ma, v)
                v /= 10
        
        if ma == 0:
            return 0
        return len(str(ma))
```
