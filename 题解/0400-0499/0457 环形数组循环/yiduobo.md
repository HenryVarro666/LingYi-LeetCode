---
title: "457. 环形数组循环"
aliases: ["yiduobo的每日leetcode 457.环形数组循环"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/218235301"
zhihu_id: "218235301"
zhihu_title: "yiduobo的每日leetcode 457.环形数组循环"
question_id: "457"
question: "环形数组循环"
problem_url: "https://leetcode.cn/problems/circular-array-loop/"
created: "2020-09-05T22:33:00+08:00"
updated: "2020-09-05T22:33:00+08:00"
upvotes: 0
comments: 0
---

# 457. 环形数组循环

> **[yiduobo的每日leetcode 457.环形数组循环](https://zhuanlan.zhihu.com/p/218235301) · 知乎 · 2020-09-05 · 赞同 0**
> 力扣：[457. 环形数组循环](https://leetcode.cn/problems/circular-array-loop/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

457.环形数组循环<https://leetcode-cn.com/problems/circular-array-loop/>

直接在数组里面不断行走直到无法继续往后走为止。无法往后走的情况有三种：

1、走回当前轮次中的点：此时说明数组中存在循环，直接返回true即可

2、走到反方向的点：根据规则不能反向行动，因此此时直接停止

3、走到之前轮次用过的点：之前轮次找不到循环，因此走到之前轮次的点之后也只能是重复之前轮次的路径，必然形成不了循环，因此此时也应该直接停止

于是现在的问题就变成了如何标记当前以及之前轮次用过的点。注意到题目保证nums中的所有数都小于等于1000，那么在用过一个点之后，将其标记为1000 + cnt，其中cnt为当前的轮次。那么如果走到的下一个点标记大于1000，那么将其标记减去1000得到其轮次cnt。若cnt与当前轮次一致，说明走回了当前轮次中的点，否则就是走到了之前轮次用过的点。

最后附上python代码：

```python
class Solution(object):
    def circularArrayLoop(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        for index in range(len(nums)):
            if nums[index] < 0:
                nums[index] = -(-nums[index] % len(nums))
            else:
                nums[index] %= len(nums)

        cnt = 0
        for index, num in enumerate(nums):
            if num > 1000:
                continue

            next_pos = (index + num + len(nums)) % len(nums)
            if next_pos == index:
                cnt += 1
                nums[index] = 1000 + cnt
                continue

            now = index
            cnt += 1
            while next_pos != index and nums[next_pos] <= 1000 and nums[next_pos] * nums[now] > 0:
                nums[now] = 1000 + cnt
                now = next_pos
                next_pos = (now + nums[now] + len(nums)) % len(nums)
            
            if next_pos == index or nums[next_pos] == nums[index]:
                return True
            
            nums[now] = 1000 + cnt
```
