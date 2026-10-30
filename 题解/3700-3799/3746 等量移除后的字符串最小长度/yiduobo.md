---
title: "3746. 等量移除后的字符串最小长度"
aliases: ["yiduobo的每日leetcode 3746.等量移除后的字符串最小长度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1973427947969991023"
zhihu_id: "1973427947969991023"
zhihu_title: "yiduobo的每日leetcode 3746.等量移除后的字符串最小长度"
question_id: "3746"
question: "等量移除后的字符串最小长度"
problem_url: "https://leetcode.cn/problems/minimum-string-length-after-balanced-removals/"
difficulty: "Medium"
rating: 1327
created: "2025-11-16T16:38:04+08:00"
updated: "2025-11-16T16:38:04+08:00"
upvotes: 2
comments: 0
---

# 3746. 等量移除后的字符串最小长度

> **[yiduobo的每日leetcode 3746.等量移除后的字符串最小长度](https://zhuanlan.zhihu.com/p/1973427947969991023) · 知乎 · 2025-11-16 · 赞同 2**
> 力扣：[3746. 等量移除后的字符串最小长度](https://leetcode.cn/problems/minimum-string-length-after-balanced-removals/) · Medium · 灵茶山艾府：[脑筋急转弯，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3746.等量移除后的字符串最小长度

[3746. 等量移除后的字符串最小长度 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-string-length-after-balanced-removals/description/)

题目给出一个仅由'a'和'b'组成的字符串s，现在可以反复移除其中的任意子串，不过移除的子串中'a'和'b'的数量必须相同。每次移除后，剩余部分的字符串会无缝拼接到一起。

问经过任意次数的移除操作后，剩余字符串的最小可能长度是多少。

当字符串中还存在两种字符时，必然存在至少一组相邻字符是由'a'和'b'组成的，于是可以不断移除掉这一组相邻的字符，直到字符串中仅剩'a'或者仅剩'b'为止。

换言之，本题的最终答案就是'a'和'b'数量之差的绝对值，于是只需一趟遍历，统计'a'和'b'出现次数之差即可。

最后附上python代码：

```python
class Solution(object):
    def minLengthAfterRemovals(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        res = 0
        for c in s:
            if c == 'a':
                res += 1
            else:
                res -= 1
        
        return abs(res)
```
