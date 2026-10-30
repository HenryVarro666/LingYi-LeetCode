---
title: "1234. 替换子串得到平衡字符串"
aliases: ["yiduobo的每日leetcode 1234.替换子串得到平衡字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/384425421"
zhihu_id: "384425421"
zhihu_title: "yiduobo的每日leetcode 1234.替换子串得到平衡字符串"
question_id: "1234"
question: "替换子串得到平衡字符串"
problem_url: "https://leetcode.cn/problems/replace-the-substring-for-balanced-string/"
difficulty: "Medium"
rating: 1878
created: "2021-06-27T14:35:46+08:00"
updated: "2021-06-27T14:35:46+08:00"
upvotes: 0
comments: 0
---

# 1234. 替换子串得到平衡字符串

> **[yiduobo的每日leetcode 1234.替换子串得到平衡字符串](https://zhuanlan.zhihu.com/p/384425421) · 知乎 · 2021-06-27 · 赞同 0**
> 力扣：[1234. 替换子串得到平衡字符串](https://leetcode.cn/problems/replace-the-substring-for-balanced-string/) · Medium · 灵茶山艾府：[滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1234.替换子串得到平衡字符串

[力扣](https://leetcode-cn.com/problems/replace-the-substring-for-balanced-string/)

题目要求替换掉字符串中的一个子串，使得最终的字符串中各个字符出现次数一致。由于这里的字符串长度是4的倍数，那么就意味着必然是有解的。简单分析下来，有三种替换方式：

1、保留尽可能长的合法前缀，替换后缀

2、保留尽可能长的合法后缀，替换前缀子

3、保留长度之和尽可能长的前缀和后缀，替换中间的部分

对于情况1和情况2都是可以使用滑动窗口解决，对于情况3则稍微复杂一点，因为需要分配前缀和后缀中字符的次数。但是换一种思路，如果我们将字符串原样复制一遍拼在后面，那么这里的前缀和后缀就能连接起来，成为这个两倍字符串中的一个连续子串，那么此时又可以使用滑动窗口来解决。当然，这里的合法字符串必然是要跨越原字符串的末尾，这样才是合法的前缀和后缀的组合。

例如字符串QWQQQQER，答案是替换掉中间的三个Q。那么我们如果将字符串拼接一份，那么就是QWQQQQERQWQQQQER，其中最长的合法，且跨越原字符串的最长得子串是QERQW，长度为5，因此最终答案就是8 - 5 \= 3。

另外，情况2也可以归类到这种情况当中一并实现。

最后附上python代码：

```python
class Solution(object):
    def balancedString(self, s):
        """
        :type s: str
        :rtype: int
        """

        cnt = {'Q':0, 'W':0, 'E':0, 'R':0}
        n = len(s)
        l = 0
        for r, char in enumerate(s):
            cnt[char] += 1
            if cnt[char] > n / 4:
                break
        
        if cnt[char] <= n / 4:
            return 0
        
        cnt[char] -= 1
        r -= 1
        res = n - (r - l + 1)
        s += s
        while l < n:
            cnt[s[l]] -= 1
            l += 1
            while cnt[s[r + 1]] < n / 4:
                r += 1
                cnt[s[r]] += 1

            if r >= n - 1 and n - (r - l + 1) < res:
                res = n - (r - l + 1)
        return res
```
