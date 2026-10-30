---
title: "3983. 一次替换后的子序列"
aliases: ["yiduobo的每日leetcode 3983.一次替换后的子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/recursion", "leetcode/memoization", "leetcode/two-pointers", "leetcode/dynamic-programming", "题单/滑动窗口与双指针", "题单/动态规划", "题单/滑动窗口与双指针/四-双序列双指针", "题单/动态规划/六-状态机-DP", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2057221650836464434"
zhihu_id: "2057221650836464434"
zhihu_title: "yiduobo的每日leetcode 3983.一次替换后的子序列"
question_id: "3983"
question: "一次替换后的子序列"
problem_url: "https://leetcode.cn/problems/subsequence-after-one-replacement/"
difficulty: "Medium"
rating: 1755
created: "2026-07-07T21:14:33+08:00"
updated: "2026-07-07T21:14:37+08:00"
upvotes: 1
comments: 0
---

# 3983. 一次替换后的子序列

> **[yiduobo的每日leetcode 3983.一次替换后的子序列](https://zhuanlan.zhihu.com/p/2057221650836464434) · 知乎 · 2026-07-07 · 赞同 1**
> 力扣：[3983. 一次替换后的子序列](https://leetcode.cn/problems/subsequence-after-one-replacement/) · Medium · 灵茶山艾府：[两种方法：前后缀分解 / 状态机 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3983.一次替换后的子序列

<https://leetcode.cn/problems/subsequence-after-one-replacement/description/>

题目给出两个由小写英文字母组成的字符串s和t。

现在最多可以选择s中的一个下标，并将该下标处的字符替换为任意小写英文字母。

若可以使得s成为t的一个子序列，那么就返回true，否则返回false。

首先，执行操作显然是有利无害的，那么在这里不妨考虑，假设操作执行的位置是index，那么如何判断执行完之后的s是否能成为t的子序列。一个直观的想法就是，以index为界，s[0]到s[index - 1]这个前缀，必须是t某个前缀的子序列，而s[index + 1]到s[-1]这个后缀必须是t某个后缀的子序列，同时，t中的前缀和后缀间，必须至少有一个空位的间隔，因为还有修改后的s[index]需要用过中间这一段间隔中的某个字符来匹配。

为了使得前缀与后缀之间留有余地的可能性尽可能的大，在这里就应该想办法找出t中尽量短的前缀与后缀，来适配被划分出去的s的前缀和后缀。对于这个问题，则可以正反两趟遍历，使用贪心解决。

以前缀为例。使用数组prefix记录t中每个匹配位置，即prefix[p]表示的是可以从t到下标prefix[p]为止的前缀中找出一个子序列，其恰好就是s[0]到s[p]。接下来只需对t进行一趟遍历，使用一个变量p记录s下一个待匹配的字符。若当前遍历到的字符t[index]与s[p]相同，那么就将index加入到prefix中，然后将p加上1即可。重复此过程直到遍历完字符串t或者p来到s的末尾。

同样的，只需反向一趟遍历，就可以计算出最优的后缀匹配位置suffix。

得到prefix和suffix后，只需再进行一趟遍历，枚举修改的位置index，那么t的前缀需要匹配的字符数量就是s[0]到s[index - 1]这一共index个，后缀需要匹配的字符就是len(s) - index - 1个。此时只需检测prefix[index]与suffix[len(s) - index - 2]是否存在，且前者与后者之间是否存在至少一个空位，若符合，则返回true。若遍历完还没找到可行的index，则返回false。

最后附上python代码：

```python
class Solution(object):
    def canMakeSubsequence(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        
        prefix = []
        suffix = []

        p = 0
        for index in range(len(t)):
            if p < len(s) and s[p] == t[index]:
                prefix.append(index)
                p += 1
        
        if p == len(s):
            return True

        p = len(s) - 1
        for index in range(len(t) - 1, -1, -1):
            if p >= 0 and s[p] == t[index]:
                suffix.append(index)
                p -= 1
        
        for index in range(len(s)):
            if index > 0:
                if len(prefix) < index:
                    left = len(t)
                else:
                    left = prefix[index - 1]
            else:
                left = -1

            if index < len(s) - 1:
                if len(suffix) < len(s) - index - 1:
                    right = -1
                else:
                    right = suffix[len(s) - index - 2]
            else:
                right = len(t)

            if left + 1 < right:
                return True
            

        
        return False
```
