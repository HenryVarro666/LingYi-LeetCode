---
title: "3039. 进行操作使字符串为空"
aliases: ["yiduobo的每日leetcode 3039.进行操作使字符串为空"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695832239"
zhihu_id: "695832239"
zhihu_title: "yiduobo的每日leetcode 3039.进行操作使字符串为空"
question_id: "3039"
question: "进行操作使字符串为空"
problem_url: "https://leetcode.cn/problems/apply-operations-to-make-string-empty/"
difficulty: "Medium"
created: "2024-05-03T22:18:23+08:00"
updated: "2024-05-03T22:18:23+08:00"
upvotes: 1
comments: 0
---

# 3039. 进行操作使字符串为空

> **[yiduobo的每日leetcode 3039.进行操作使字符串为空](https://zhuanlan.zhihu.com/p/695832239) · 知乎 · 2024-05-03 · 赞同 1**
> 力扣：[3039. 进行操作使字符串为空](https://leetcode.cn/problems/apply-operations-to-make-string-empty/) · Medium · 灵茶山艾府：[统计字母出现次数和最后一次出现的下标（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3039.进行操作使字符串为空

[. - 力扣（LeetCode）](https://leetcode.cn/problems/apply-operations-to-make-string-empty/description/)

由于题目每轮操作都会移除每种字符各一个，因此倒数第二轮剩下的必然是出现次数最多的字符。另一方面，由于移除的操作使从前往后进行的，因此倒数第二轮剩下的字符必然是其所有出现位置中最靠后的那个，因此最终答案中各字符的相对顺序就取决于其出现在原字符串中的最后那个位置。

于是只需一趟遍历，一边统计每种字符出现的次数，一边记录每种字符最后一次出现的位置。接下来取出出现次数最多的字符集，按照最后一次出现的位置排序即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def lastNonEmptyString(self, s):
        """
        :type s: str
        :rtype: str
        """

        freq = Counter()
        last = {}
        for index, char in enumerate(s):
            freq[char] += 1
            last[char] = index
        ma = max(freq.values())

        rest = set()
        for char in freq:
            if freq[char] == ma:
                rest.add(char)
        
        return ''.join(sorted(list(rest), key=lambda d:last[d]))
```
