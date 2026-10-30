---
title: "2379. 得到K个黑块的最少涂色次数"
aliases: ["yiduobo的每日leetcode 2379.得到K个黑块的最少涂色次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/two-pointers", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/564515109"
zhihu_id: "564515109"
zhihu_title: "yiduobo的每日leetcode 2379.得到K个黑块的最少涂色次数"
question_id: "2379"
question: "得到 K 个黑块的最少涂色次数"
problem_url: "https://leetcode.cn/problems/minimum-recolors-to-get-k-consecutive-black-blocks/"
difficulty: "Easy"
rating: 1360
created: "2022-09-15T03:19:26+08:00"
updated: "2022-09-15T03:19:26+08:00"
upvotes: 1
comments: 0
---

# 2379. 得到K个黑块的最少涂色次数

> **[yiduobo的每日leetcode 2379.得到K个黑块的最少涂色次数](https://zhuanlan.zhihu.com/p/564515109) · 知乎 · 2022-09-15 · 赞同 1**
> 力扣：[2379. 得到 K 个黑块的最少涂色次数](https://leetcode.cn/problems/minimum-recolors-to-get-k-consecutive-black-blocks/) · Easy · 灵茶山艾府：[滑动窗口+避免分支预测（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2379.得到K个黑块的最少涂色次数

[力扣](https://leetcode.cn/problems/minimum-recolors-to-get-k-consecutive-black-blocks/)

使用一个长度为k的滑动窗口从左向右滑就行了，维护窗口内白色块的数量cnt。cnt越小，需要涂黑的色块就越少，因此取窗口滑动过程中cnt的最小值作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def minimumRecolors(self, blocks, k):
        """
        :type blocks: str
        :type k: int
        :rtype: int
        """

        cnt = 0
        for index in range(k):
            if blocks[index] == 'W':
                cnt += 1
        
        res = cnt
        for index in range(k, len(blocks)):
            if blocks[index] == 'W':
                cnt += 1
            if blocks[index - k] == 'W':
                cnt -= 1
            
            res = min(res, cnt)
            
        return res
```
