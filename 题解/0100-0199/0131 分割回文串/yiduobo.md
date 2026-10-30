---
title: "131. 分割回文串"
aliases: ["yiduobo的每日leetcode 131.分割回文串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/链表-二叉树与回溯/四-回溯", "题单/LeetCode-热题-100/回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/141249547"
zhihu_id: "141249547"
zhihu_title: "yiduobo的每日leetcode 131.分割回文串"
question_id: "131"
question: "分割回文串"
problem_url: "https://leetcode.cn/problems/palindrome-partitioning/"
difficulty: "Medium"
created: "2020-05-15T21:47:34+08:00"
updated: "2020-05-15T21:55:51+08:00"
upvotes: 0
comments: 0
---

# 131. 分割回文串

> **[yiduobo的每日leetcode 131.分割回文串](https://zhuanlan.zhihu.com/p/141249547) · 知乎 · 2020-05-15 · 赞同 0**
> 力扣：[131. 分割回文串](https://leetcode.cn/problems/palindrome-partitioning/) · Medium · 灵茶山艾府：[【视频】回溯不会写？套路在此！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

131.分割回文串<https://leetcode-cn.com/problems/palindrome-partitioning/>

搜索回溯的题目。

每次枚举分割点，然后检测分割出的部分是否是回文串，如果是回文串那么继续分割剩下的部分即可。

需要注意的是，所有子串是否是回文串从一开始就确定下来了，因此可以先进行预处理，或者使用记忆化搜索的方式将是否回文记录下来。

我在这里采用的是记忆化搜索的方式，f[left][right]表示s中的left到right这一段是否是回文串，那么：

1、left等于right：此时只有一个字符，因此有f[left][right] \= True。

2、left大于right：此时为空串，因此有f[left][right] \= True。

3、否则判断s[left]是否等于s[right]：

若不相等，说明不是回文串，则f[left][right] \= False。

若相等，那么需要先递归计算f[left + 1][right - 1]的情况，然后f[left][right]就等于f[left + 1][right - 1]。

最后附上python代码，dfs为枚举分割点的搜索回溯，check则是记忆化搜索检测回文：

```python
class Solution(object):
    def partition(self, s):
        """
        :type s: str
        :rtype: List[List[str]]
        """

        res = []
        f = [[None] * len(s) for _ in range(len(s))]
        self.dfs(s, 0, f, [], res)
        return res

    def dfs(self, s, left, f, now, res):
        if len(s) == left:
            res.append(now[:])
            return

        for index in range(left, len(s)):
            if self.check(s, left, index, f):
                now.append(s[left : index + 1])
                self.dfs(s, index + 1, f, now, res)
                now.pop()

    def check(self, s, left, right, f):
        if f[left][right] is None:
            if left >= right:
                f[left][right] = True
            else:
                if s[left] == s[right]:
                    f[left][right] = self.check(s, left + 1, right - 1, f)
                else:
                    f[left][right] = False

        return f[left][right]
```
