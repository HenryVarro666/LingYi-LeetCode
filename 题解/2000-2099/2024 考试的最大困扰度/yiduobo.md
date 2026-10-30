---
title: "2024. 考试的最大困扰度"
aliases: ["yiduobo的每日leetcode 2024.考试的最大困扰度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/507465816"
zhihu_id: "507465816"
zhihu_title: "yiduobo的每日leetcode 2024.考试的最大困扰度"
question_id: "2024"
question: "考试的最大困扰度"
problem_url: "https://leetcode.cn/problems/maximize-the-confusion-of-an-exam/"
difficulty: "Medium"
rating: 1643
created: "2022-04-29T21:24:56+08:00"
updated: "2022-04-29T21:24:56+08:00"
upvotes: 0
comments: 0
---

# 2024. 考试的最大困扰度

> **[yiduobo的每日leetcode 2024.考试的最大困扰度](https://zhuanlan.zhihu.com/p/507465816) · 知乎 · 2022-04-29 · 赞同 0**
> 力扣：[2024. 考试的最大困扰度](https://leetcode.cn/problems/maximize-the-confusion-of-an-exam/) · Medium · 灵茶山艾府：[最大滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2024.考试的最大困扰度

[力扣](https://leetcode-cn.com/problems/maximize-the-confusion-of-an-exam/)

经典的双指针问题。

首先需要确定是尽量使得连续的T最多，还是连续的F最多。当确定了选择的字符char后，就可以利用双指针来求出最长连续的区间。每一轮，都将右边界r向右移动一个位置，对于新加入的字符：

1、若新加入的字符与char一致，那么左边界l不需要变动

2、若新加入的字符与char一致，且此时区间l到r直接不是char的字符数目不超过k个，那么此时左边界l同样不需要变动

3、若新加入的字符与char不一致，且此时区间l到r之间不是char的字符已经达到了k + 1个，此时就需要不断将l向右移动，直到l大于r，或者有某个不是char的字符因为l的向右移动被排除出了区间

无论哪种情况，都需要使用此时的l和r来更新最终的答案

分别求解char为'F'以及char为'T'时的答案，取其中的较大值作为最终答案返回即可。

最后附上python代码：

```python
class Solution(object):
    def maxConsecutiveAnswers(self, answerKey, k):
        """
        :type answerKey: str
        :type k: int
        :rtype: int
        """

        n = len(answerKey)

        def check(char):
            l = 0
            r = -1
            cnt = 0
            res = 0
            while r + 1 < n:
                r += 1
                if answerKey[r] != char:
                    cnt += 1
                    if cnt > k:
                        while l <= r and answerKey[l] == char:
                            l += 1
                        cnt -= 1
                        l += 1
                
                res = max(res, r - l + 1)

            return res

        return max(check('T'), check('F'))
```
