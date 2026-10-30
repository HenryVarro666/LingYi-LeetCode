---
title: "1980. 找出不同的二进制字符串"
aliases: ["yiduobo的每日leetcode 1980.找出不同的二进制字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "leetcode/enumeration", "leetcode/bao-li", "题单/贪心算法", "题单/贪心算法/六-构造题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/497535128"
zhihu_id: "497535128"
zhihu_title: "yiduobo的每日leetcode 1980.找出不同的二进制字符串"
question_id: "1980"
question: "找出不同的二进制字符串"
problem_url: "https://leetcode.cn/problems/find-unique-binary-string/"
difficulty: "Medium"
created: "2022-04-13T01:00:32+08:00"
updated: "2022-04-13T01:00:32+08:00"
upvotes: 0
comments: 0
---

# 1980. 找出不同的二进制字符串

> **[yiduobo的每日leetcode 1980.找出不同的二进制字符串](https://zhuanlan.zhihu.com/p/497535128) · 知乎 · 2022-04-13 · 赞同 0**
> 力扣：[1980. 找出不同的二进制字符串](https://leetcode.cn/problems/find-unique-binary-string/) · Medium · 灵茶山艾府：[两种方法：暴力枚举 / 康托对角线（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1980.找出不同的二进制字符串

[力扣](https://leetcode-cn.com/problems/find-unique-binary-string/)

注意到题目中n的规模很小，因此我在这里直接使用的暴力算法。将nums中的每个数加入到集合中，然后从0开始向上枚举，找出一个没有出现在集合中的数，再将其转化成二进制串返回即可。

最后附上python代码：

```python
class Solution(object):
    def findDifferentBinaryString(self, nums):
        """
        :type nums: List[str]
        :rtype: str
        """

        num_set = set()
        for num in nums:
            now = 0
            for char in num:
                now = now * 2 + int(char)
            
            num_set.add(now)
        
        now = 0
        while now in num_set:
            now += 1
        
        res = []
        for _ in range(len(nums)):
            res.append(str(now % 2))
            now /= 2
        
        res.reverse()
        return ''.join(res)
```
