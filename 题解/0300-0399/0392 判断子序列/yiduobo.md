---
title: "392. 判断子序列"
aliases: ["yiduobo的每日leetcode 392.判断子序列"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "leetcode/dynamic-programming", "题单/滑动窗口与双指针", "题单/面试经典-150-题", "题单/滑动窗口与双指针/四-双序列双指针", "题单/面试经典-150-题/双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/174836998"
zhihu_id: "174836998"
zhihu_title: "yiduobo的每日leetcode 392.判断子序列"
question_id: "392"
question: "判断子序列"
problem_url: "https://leetcode.cn/problems/is-subsequence/"
difficulty: "Easy"
created: "2020-08-08T23:58:40+08:00"
updated: "2020-08-08T23:58:40+08:00"
upvotes: 0
comments: 0
---

# 392. 判断子序列

> **[yiduobo的每日leetcode 392.判断子序列](https://zhuanlan.zhihu.com/p/174836998) · 知乎 · 2020-08-08 · 赞同 0**
> 力扣：[392. 判断子序列](https://leetcode.cn/problems/is-subsequence/) · Easy · 灵茶山艾府：[简洁写法，附进阶问题解答（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

392.判断子序列<https://leetcode-cn.com/problems/is-subsequence/submissions/>

比较基础的题目，需要用到贪心的思想。

由于是子序列，那么不要求t中的字符是连续的，那么对于s[i]，若存在j和k，满足

t[j] \= t[k] \= s[i]，且j \< k，那么此时我们选择t[j]来匹配s[i]显然是更好的，因为若是通t[k]匹配能得到结果的话，将t[k]改为t[j]也能得到结果，反过来则不一定。

于是我们可以使用两个指针分别从s和t的头部开始往后扫描，当匹配成功时则往后移动s的指针，而t的指针则是每一次都需要往后移动。最终的时间复杂度为O(m + n)。

题目中的后续挑战，存在大量s时，注意到题目保证s和t中只存在小写字符，因此我们可以对于t中每个字符，预处理出所有小写字符下一次出现的位置。

设f[i][char]表示字符串t中，在位置i之后第一次出现char的位置。对于f[i]，我们可以知道字符t[i +1]下一次出现在i + 1的位置，而其他字符下一次出现的位置则可以通过f[i + 1]获取到，于是我们可以使用动态规划从后往前进行计算。预处理的时间复杂度为O(26m)

那么一趟预处理之后，对于后续的每个s就可以通过f在t中进行跳跃，直到匹配完成或者匹配失败，于是最终的时间复杂度为O(kn)，其中k为询问的次数。

那么最终总的时间复杂度为O(26m + kn)

最后附上python代码：

```python
class Solution(object):
    def isSubsequence(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """

        f = [[None] * 26 for _ in range(len(t) + 1)]
        for index in range(len(t) - 1, -1, -1):
            f[index] = f[index + 1][:]
            f[index][ord(t[index]) - 97] = index + 1

        now = 0
        for char in s:
            now = f[now][ord(char) - 97]
            if not now:
                return False

        return True
```
