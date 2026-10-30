---
title: "696. 计算二进制子串"
aliases: ["yiduobo的每日leetcode 696.计算二进制子串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/314241462"
zhihu_id: "314241462"
zhihu_title: "yiduobo的每日leetcode 696.计算二进制子串"
question_id: "696"
question: "计数二进制子串"
problem_url: "https://leetcode.cn/problems/count-binary-substrings/"
difficulty: "Easy"
created: "2020-11-26T22:28:25+08:00"
updated: "2020-11-26T22:28:25+08:00"
upvotes: 0
comments: 0
---

# 696. 计算二进制子串

> **[yiduobo的每日leetcode 696.计算二进制子串](https://zhuanlan.zhihu.com/p/314241462) · 知乎 · 2020-11-26 · 赞同 0**
> 力扣：[696. 计数二进制子串](https://leetcode.cn/problems/count-binary-substrings/) · Easy · 灵茶山艾府：[一次遍历，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

696.计算二进制子串

[力扣](https://leetcode-cn.com/problems/count-binary-substrings/)

题目要求统计所有形如11..1100..00的子串个数，注意到这里的1和0都必须挨在一起，那么假设现在有m个连续的1和n个连续的0组成的字符串，那么我们从1和0的交界处开始往外扩展，就可以得到10、1100、111000、...、11..1100..00，最后这里1和0的个数必然是min(m, n)，因此我们可以从中得到min(m, n)个符合条件的子串。

有了这个结论，我们就可以从头开始往后扫描，交替统计当前连续1或连续0的个数，取二者的较小值累加到答案当中即可。

最后附上python代码：

```python
class Solution(object):
    def countBinarySubstrings(self, s):
        """
        :type s: str
        :rtype: int
        """

        last_len = 0
        last_pos = 0
        n = len(s)
        res = 0

        while last_pos < n:
            pos = last_pos + 1
            while pos < n and s[pos] == s[last_pos]:
                pos += 1
            res += min(last_len, pos - last_pos)
            last_len = pos - last_pos
            last_pos = pos
        
        return res
```
