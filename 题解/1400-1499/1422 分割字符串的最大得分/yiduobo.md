---
title: "1422. 分割字符串的最大得分"
aliases: ["yiduobo的每日leetcode 1422.分割字符串的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/enumeration", "leetcode/bian-li", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/408018138"
zhihu_id: "408018138"
zhihu_title: "yiduobo的每日leetcode 1422.分割字符串的最大得分"
question_id: "1422"
question: "分割字符串的最大得分"
problem_url: "https://leetcode.cn/problems/maximum-score-after-splitting-a-string/"
difficulty: "Easy"
created: "2021-09-07T23:54:06+08:00"
updated: "2021-09-07T23:54:06+08:00"
upvotes: 0
comments: 0
---

# 1422. 分割字符串的最大得分

> **[yiduobo的每日leetcode 1422.分割字符串的最大得分](https://zhuanlan.zhihu.com/p/408018138) · 知乎 · 2021-09-07 · 赞同 0**
> 力扣：[1422. 分割字符串的最大得分](https://leetcode.cn/problems/maximum-score-after-splitting-a-string/) · Easy · 灵茶山艾府：[枚举分割线，O(n) 前后缀分解 / 一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1422.分割字符串的最大得分

[力扣](https://leetcode-cn.com/problems/maximum-score-after-splitting-a-string/)

比较基础的题目，可以直接一趟扫描枚举分割点，分别统计左侧0的数目和右侧1的数目。

统计的时候有一个小技巧。设所有1的数目cnt_one，那么对于长度为l的左侧字符串中，若有cnt_zero个0，那么左侧字符串中1的数目就是l - cnt_zero，这样一来右侧字符串中1的数目就是cnt_one - (l - cnt_zero)了，于是此时的得分就是

cnt_zero + cnt_one - (l - zero) \= cnt_zero \* 2 - l + cnt_one

由于这里的cnt_one是常量，为了使得得分最高，实际上就是要让cnt_zero \* 2 - l 这一项最大。因此我们只需要一趟扫描找出最大值，顺便在扫描过程中统计1的数目即可。

需要特别注意的是，题目要求分割的结果是两个非空串，因此我们需要将答案初始化为左串长度为1的情况，计算则只能到len(s) - 2的位置就停止，同时需要记得用s的最后一个字符去更新cnt_one。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, s):
        """
        :type s: str
        :rtype: int
        """

        cnt_one = 0
        cnt_zero = 0
        res = None
        for index in range(len(s) - 1):
            char = s[index]
            if char == '0':
                cnt_zero += 1
            else:
                cnt_one += 1
            
            if res is None or res < cnt_zero + cnt_zero - (index + 1):
                res = cnt_zero + cnt_zero - (index + 1)
        
        if s[-1] == '1':
            cnt_one += 1

        return res + cnt_one
```
