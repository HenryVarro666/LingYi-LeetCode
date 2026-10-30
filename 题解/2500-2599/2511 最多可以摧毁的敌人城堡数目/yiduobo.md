---
title: "2511. 最多可以摧毁的敌人城堡数目"
aliases: ["yiduobo的每日leetcode 2511.最多可以摧毁的敌人城堡数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634316368"
zhihu_id: "634316368"
zhihu_title: "yiduobo的每日leetcode 2511.最多可以摧毁的敌人城堡数目"
question_id: "2511"
question: "最多可以摧毁的敌人城堡数目"
problem_url: "https://leetcode.cn/problems/maximum-enemy-forts-that-can-be-captured/"
difficulty: "Easy"
created: "2023-06-04T21:48:06+08:00"
updated: "2023-06-04T21:48:06+08:00"
upvotes: 0
comments: 0
---

# 2511. 最多可以摧毁的敌人城堡数目

> **[yiduobo的每日leetcode 2511.最多可以摧毁的敌人城堡数目](https://zhuanlan.zhihu.com/p/634316368) · 知乎 · 2023-06-04 · 赞同 0**
> 力扣：[2511. 最多可以摧毁的敌人城堡数目](https://leetcode.cn/problems/maximum-enemy-forts-that-can-be-captured/) · Easy · 灵茶山艾府：[一次遍历（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2511.最多可以摧毁的敌人城堡数目

[力扣](https://leetcode.cn/problems/maximum-enemy-forts-that-can-be-captured/)

题目要求找出一段最长的连续0，这段0的两侧分别为1和-1。对于本题，只需一趟遍历，使用两个变量pre_v和pre_index分别记录最后一次出现的是1还是-1，以及其具体的下标位置。

对于当前遍历到的位置index：

1、若forts[index]的值为1或者-1，那么就检测forts[index]与pre_v之和是否为0。若为0，说明当前位置与pre_index之间这一段连续的0是一组可行解，此时应该使用这一段0的长度来更新最终答案。若不为0，则无事发生。无论是哪种情况，都应该使用forts[index]以及index来更新prev_v以及prev_index。

2、若forst[index]的值为0，此时无需进行任何处理，继续向后遍历即可。

最后python代码：

```python
class Solution(object):
    def captureForts(self, forts):
        """
        :type forts: List[int]
        :rtype: int
        """

        pre_v = 0
        pre_pos = None
        res = 0

        for index, v in enumerate(forts):
            if v == 1 or v == -1:
                if v + pre_v == 0:
                    res = max(res, index - pre_pos - 1)
                pre_v = v
                pre_pos = index

        return res
```
