---
title: "487. 最大连续1的个数II"
aliases: ["yiduobo的每日leetcode 487.最大连续1的个数II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/600308501"
zhihu_id: "600308501"
zhihu_title: "yiduobo的每日leetcode 487.最大连续1的个数II"
question_id: "487"
question: "最大连续1的个数II"
problem_url: "https://leetcode.cn/problems/max-consecutive-ones-ii/"
created: "2023-01-20T23:37:04+08:00"
updated: "2023-01-20T23:37:04+08:00"
upvotes: 0
comments: 0
---

# 487. 最大连续1的个数II

> **[yiduobo的每日leetcode 487.最大连续1的个数II](https://zhuanlan.zhihu.com/p/600308501) · 知乎 · 2023-01-20 · 赞同 0**
> 力扣：[487. 最大连续1的个数II](https://leetcode.cn/problems/max-consecutive-ones-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

487.最大连续1的个数II

[力扣](https://leetcode.cn/problems/max-consecutive-ones-ii/)

最终答案可能有以下四种可能：

1、不进行任何操作，就只有一整段1

2、一段连续的1左侧存在一个0，对这个0进行一次操作

3、一段连续的1右侧存在一个0，对这个0进行一次操作

4、两端连续的1之间由一个0隔开，对这个0进行一次操作，将这两段1合并成一段

如果希望在一趟遍历内解决问题，那么为了处理情况4，在储存当前遍历到的这一段1之外，还需要使用一个遍历储存在当前这一段1之前，跳过一个0之后的连续1的数量。分别记当前这一段1的数量和跳过之前一个0之后的连续1的数量为now和last，二者的初始值分别为0和none。接下来一趟遍历，对于当前遍历到数num：

若num为1，那么首先需要将now加上1。接下来，若last不为空，说明在当前这一段连续的1之前是存在0的，那么可以使用上面情况2和情况4来更新最终答案。可以发现，情况4显然是比情况2要更优的，因此在这里只需要使用情况4来更新答案。反过来，若last为空，说明这段1左侧不存在0，因此只能使用情况1来更新答案。

若num为0，那么就应该将last更新为now，并将now更新为0。这种情况下，新的last配合上当前这个0，就是情况3，因此可以用情况3来更新答案。

最后附上python代码：

```python
class Solution(object):
    def findMaxConsecutiveOnes(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        last = None
        now = 0
        res = 0
        for num in nums:
            if num == 1:
                now += 1
                if last is not None:
                    res = max(res, last + now + 1)
                else:
                    res = max(res, now)
            else:
                last = now
                now = 0
                res = max(res, last + 1)
        
        return res
```
