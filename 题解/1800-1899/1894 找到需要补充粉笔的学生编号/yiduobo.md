---
title: "1894. 找到需要补充粉笔的学生编号"
aliases: ["yiduobo的每日leetcode 1894.找到需要补充粉笔的学生编号"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/479033381"
zhihu_id: "479033381"
zhihu_title: "yiduobo的每日leetcode 1894.找到需要补充粉笔的学生编号"
question_id: "1894"
question: "找到需要补充粉笔的学生编号"
problem_url: "https://leetcode.cn/problems/find-the-student-that-will-replace-the-chalk/"
difficulty: "Medium"
created: "2022-03-11T00:12:25+08:00"
updated: "2022-03-11T00:12:26+08:00"
upvotes: 1
comments: 0
---

# 1894. 找到需要补充粉笔的学生编号

> **[yiduobo的每日leetcode 1894.找到需要补充粉笔的学生编号](https://zhuanlan.zhihu.com/p/479033381) · 知乎 · 2022-03-11 · 赞同 1**
> 力扣：[1894. 找到需要补充粉笔的学生编号](https://leetcode.cn/problems/find-the-student-that-will-replace-the-chalk/) · Medium · 灵茶山艾府：[Go 模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1894.找到需要补充粉笔的学生编号

[力扣](https://leetcode-cn.com/problems/find-the-student-that-will-replace-the-chalk/)

首先，若当前粉笔数大于所有学生都回答一次问题消耗的粉笔数之后，那么说明部分学生可能需要回答两次或者多次问题，于是在这里可以先将k对所有学生都回答一次问题消耗的粉笔数取模，然后再进行判断。

对于第i个学生，到该学生之前消耗的粉笔总数为chalk[0] + chalk[1] + ... + chalk[i - 1]，而之后的消耗则为chalk[0] + chalk[1] + ... + chalk[i]。可以发现这是两个前缀和，分别记为s[i - 1]以及s[i]，那么题目实际上就是要找到一个i，满足s[i - 1] \<\= k \< s[i]，于是在这里可以先将前缀和全部计算出来，然后在其中二分取模后的k，从而找到最终答案i。

另外，二分时需要注意边界情况，当k \< s[0]时，则说明答案就是0，此时不需要进行二分。

最后附上python代码：

```python
class Solution(object):
    def chalkReplacer(self, chalk, k):
        """
        :type chalk: List[int]
        :type k: int
        :rtype: int
        """

        s = [chalk[0]]
        for num in chalk[1:]:
            s.append(s[-1] + num)
        
        k %= s[-1]
        if k < s[0]:
            return 0
        
        l = 0
        r = len(chalk) - 1
        while l < r:
            mid = (l + r) >> 1
            if s[mid] > k:
                r = mid
            else:
                l = mid + 1
        
        return l
```
