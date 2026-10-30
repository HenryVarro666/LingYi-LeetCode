---
title: "3135. 通过添加或删除结尾字符来同化字符串"
aliases: ["yiduobo的每日leetcode 3135.通过添加或删除结尾字符来同化字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/702527641"
zhihu_id: "702527641"
zhihu_title: "yiduobo的每日leetcode 3135.通过添加或删除结尾字符来同化字符串"
question_id: "3135"
question: "通过添加或删除结尾字符来同化字符串"
problem_url: "https://leetcode.cn/problems/equalize-strings-by-adding-or-removing-characters-at-ends/"
created: "2024-06-10T01:19:54+08:00"
updated: "2024-06-10T01:19:54+08:00"
upvotes: 2
comments: 0
---

# 3135. 通过添加或删除结尾字符来同化字符串

> **[yiduobo的每日leetcode 3135.通过添加或删除结尾字符来同化字符串](https://zhuanlan.zhihu.com/p/702527641) · 知乎 · 2024-06-10 · 赞同 2**
> 力扣：[3135. 通过添加或删除结尾字符来同化字符串](https://leetcode.cn/problems/equalize-strings-by-adding-or-removing-characters-at-ends/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3135.通过添加或删除结尾字符来同化字符串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/equalize-strings-by-adding-or-removing-characters-at-ends/description/)

题目给出两个字符串initial和target，每次操作可以在initial的开头或末尾添加或删除一个字符，问将initial变为target所需的最少操作次数。

由于每次操作只能在initial的头部或者尾部添加或删除字符，那么就意味着initial中不需要进行操作的字符要么为空，要么是其中的一个连续子串。证明也很简单，如果不为空也不是连续子串，那么至少包含有两个部分，而对于这两个部分之间的其他字符，如果想修改这些字符，就必须修改其左侧或者右侧的字符，与左右两个部分不需要操作的前提就矛盾了。

在明确了最后无需操作的部分是一个子串后，为了使得总的操作次数最少，那么就应该让这个子串尽量长，也就是说本题实际上求解的是initial和target的最长公共子串。对于这个问题，可以采用动态规划来求解。令f[i][j]表示以initial[i - 1]结尾的子串与target[j - 1]结尾的子串可以匹配的最长长度，那么对于f[i][j]，只有当initial[i - 1] \= target[j - 1]时，才有f[i][j] \= f[i - 1][j - 1] + 1，其他情况下f[i][j]都为0。

计算完成后，设ma为f数组中的最大值，那么首先要将initial删除到只剩下ma个字符再将其扩展成target，因此总的操作次数就是initial和target的长度之和，再减去两倍的ma。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, initial, target):
        """
        :type initial: str
        :type target: str
        :rtype: int
        """

        m = len(initial)
        n = len(target)

        f = [[0] * (n + 1) for _ in range(m + 1)]
        ma = 0
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if initial[i - 1] == target[j - 1]:
                    f[i][j] = f[i - 1][j - 1] + 1
                    ma = max(ma, f[i][j])
        
        return m + n - ma * 2
```
