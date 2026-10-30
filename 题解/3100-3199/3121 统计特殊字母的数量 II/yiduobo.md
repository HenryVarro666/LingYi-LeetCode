---
title: "3121. 统计特殊字母的数量II"
aliases: ["yiduobo的每日leetcode 3121.统计特殊字母的数量II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/701635557"
zhihu_id: "701635557"
zhihu_title: "yiduobo的每日leetcode 3121.统计特殊字母的数量II"
question_id: "3121"
question: "统计特殊字母的数量 II"
problem_url: "https://leetcode.cn/problems/count-the-number-of-special-characters-ii/"
difficulty: "Medium"
created: "2024-06-04T22:36:34+08:00"
updated: "2024-06-04T22:36:34+08:00"
upvotes: 0
comments: 0
---

# 3121. 统计特殊字母的数量II

> **[yiduobo的每日leetcode 3121.统计特殊字母的数量II](https://zhuanlan.zhihu.com/p/701635557) · 知乎 · 2024-06-04 · 赞同 0**
> 力扣：[3121. 统计特殊字母的数量 II](https://leetcode.cn/problems/count-the-number-of-special-characters-ii/) · Medium · 灵茶山艾府：[两种方法：状态机 / 位运算（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3121.统计特殊字母的数量II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-the-number-of-special-characters-ii/description/)

题目给出一个字符串，要求判断其中特殊字母的数目。特殊字符指的是对于某个字符c，其大小写都在字符串中出现，且c的所有小写形式都必须出现在c的第一个大写形式之前。

对于某个字符，如果其所有小写形式都出现在第一个大写形式之前，就相当于其最后一个小写形式的下标小于第一个大小形式的下标，于是只需一趟遍历，使用两个哈希表last和first分别记录每种小写字符最后一次出现的下标，以及每种大写字符第一次出现的下标。遍历完成后，遍历last中的字符，若其对应的大写形式出现在first中，且值大于其在last中的值，就将答案加上1。

最后附上python代码：

```python
class Solution(object):
    def numberOfSpecialChars(self, word):
        """
        :type word: str
        :rtype: int
        """

        last = {}
        first = {}
        for index, char in enumerate(word):
            if 'a' <= char <= 'z':
                last[char] = index
            elif char not in first:
                first[char] = index

        res = 0
        for char in last:
            if first.get(chr(ord(char) - 32), -1) > last[char]:
                res += 1
        
        return res
```
