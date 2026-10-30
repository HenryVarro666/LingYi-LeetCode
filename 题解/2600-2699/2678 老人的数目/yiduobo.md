---
title: "2678. 老人的数目"
aliases: ["yiduobo的每日leetcode 2678.老人的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/649319060"
zhihu_id: "649319060"
zhihu_title: "yiduobo的每日leetcode 2678.老人的数目"
question_id: "2678"
question: "老人的数目"
problem_url: "https://leetcode.cn/problems/number-of-senior-citizens/"
difficulty: "Easy"
created: "2023-08-11T02:32:32+08:00"
updated: "2023-08-11T02:32:32+08:00"
upvotes: 0
comments: 0
---

# 2678. 老人的数目

> **[yiduobo的每日leetcode 2678.老人的数目](https://zhuanlan.zhihu.com/p/649319060) · 知乎 · 2023-08-11 · 赞同 0**
> 力扣：[2678. 老人的数目](https://leetcode.cn/problems/number-of-senior-citizens/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2678.老人的数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/number-of-senior-citizens/description/)

题目只关心乘客的年龄，因此只需提取乘客信息中的倒数第四位以及倒数第三位，计算出乘客的年龄并与60对比即可。

最后附上python代码：

```python
class Solution(object):
    def countSeniors(self, details):
        """
        :type details: List[str]
        :rtype: int
        """

        res = 0
        for s in details:
            if int(s[-4]) * 10 + int(s[-3]) > 60:
                res += 1
        
        return res
```
