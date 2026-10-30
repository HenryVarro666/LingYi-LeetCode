---
title: "1358. 包含所有三种字符的子字符串数目"
aliases: ["yiduobo的每日leetcode 1358.包含所有三种字符的子字符串数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/398831667"
zhihu_id: "398831667"
zhihu_title: "yiduobo的每日leetcode 1358.包含所有三种字符的子字符串数目"
question_id: "1358"
question: "包含所有三种字符的子字符串数目"
problem_url: "https://leetcode.cn/problems/number-of-substrings-containing-all-three-characters/"
difficulty: "Medium"
rating: 1646
created: "2021-08-11T22:34:30+08:00"
updated: "2021-08-11T22:34:30+08:00"
upvotes: 0
comments: 0
---

# 1358. 包含所有三种字符的子字符串数目

> **[yiduobo的每日leetcode 1358.包含所有三种字符的子字符串数目](https://zhuanlan.zhihu.com/p/398831667) · 知乎 · 2021-08-11 · 赞同 0**
> 力扣：[1358. 包含所有三种字符的子字符串数目](https://leetcode.cn/problems/number-of-substrings-containing-all-three-characters/) · Medium · 灵茶山艾府：[【模板】越长越合法型滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1358.包含所有三种字符的子字符串数目

[力扣](https://leetcode-cn.com/problems/number-of-substrings-containing-all-three-characters/)

经典的滑动窗口问题。对于起点为l的字符串，我们找出其满足条件的最小右边界r，那么以l开头，符合条件的字符串就一共有n - r个。

接下来我们将l向右移动，此时s[l]被移出了窗口，那么我们需要检测l + 1到r之间是否还有s[l]这种字符。一个简单想法就是检测在l之后，下一个s[l]出现的位置next，若next小于等于r，那么说明此时l + 1到r这个子字符串中依然有三种字符，否则我们就需要将r向后移动到next。

为了优化效率，我们应当先从后先前一趟扫描，预处理出每个字符下一次出现的位置。

最后附上python代码：

```python
class Solution(object):
    def numberOfSubstrings(self, s):
        """
        :type s: str
        :rtype: int
        """

        last_a = None
        last_b = None
        last_c = None
        next_pos = []
        n = len(s)
        for index in range(n - 1, -1, -1):
            if s[index] == 'a':
                next_pos.append(last_a)
                last_a = index
            elif s[index] == 'b':
                next_pos.append(last_b)
                last_b = index
            else:
                next_pos.append(last_c)
                last_c = index
        
        next_pos.reverse()

        if last_a is None or last_b is None or last_c is None:
            return 0
        
        l = 0
        r = max(last_a, last_b, last_c)
        res = n - r
        while l < n:
            if next_pos[l] is None:
                break
            r = max(r, next_pos[l])
            res += n - r
            l += 1

        return res
```
