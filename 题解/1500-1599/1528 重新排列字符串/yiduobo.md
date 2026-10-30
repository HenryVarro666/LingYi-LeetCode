---
title: "1528. 重新排列字符串"
aliases: ["yiduobo的每日leetcode 1528.重新排列字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/422498838"
zhihu_id: "422498838"
zhihu_title: "yiduobo的每日leetcode 1528.重新排列字符串"
question_id: "1528"
question: "重新排列字符串"
problem_url: "https://leetcode.cn/problems/shuffle-string/"
created: "2021-10-17T18:43:11+08:00"
updated: "2021-10-17T18:43:11+08:00"
upvotes: 0
comments: 0
---

# 1528. 重新排列字符串

> **[yiduobo的每日leetcode 1528.重新排列字符串](https://zhuanlan.zhihu.com/p/422498838) · 知乎 · 2021-10-17 · 赞同 0**
> 力扣：[1528. 重新排列字符串](https://leetcode.cn/problems/shuffle-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1528.重新排列字符串

[力扣](https://leetcode-cn.com/problems/shuffle-string/)

比较基础的题目，按题目意思根据indices重新排布s然后输出即可。

最后附上python代码：

```python
class Solution(object):
    def restoreString(self, s, indices):
        """
        :type s: str
        :type indices: List[int]
        :rtype: str
        """

        res = [''] * len(s)
        for index, pos in enumerate(indices):
            res[pos] = s[index]
        
        return ''.join(res)
```
