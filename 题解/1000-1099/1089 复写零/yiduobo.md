---
title: "1089. 复写零"
aliases: ["yiduobo的每日leetcode 1089.复写零"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/373112247"
zhihu_id: "373112247"
zhihu_title: "yiduobo的每日leetcode 1089.复写零"
question_id: "1089"
question: "复写零"
problem_url: "https://leetcode.cn/problems/duplicate-zeros/"
created: "2021-05-17T23:57:17+08:00"
updated: "2021-05-17T23:57:17+08:00"
upvotes: 1
comments: 0
---

# 1089. 复写零

> **[yiduobo的每日leetcode 1089.复写零](https://zhuanlan.zhihu.com/p/373112247) · 知乎 · 2021-05-17 · 赞同 1**
> 力扣：[1089. 复写零](https://leetcode.cn/problems/duplicate-zeros/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

由于1081题与316题完全一致，因此在这里直接跳过。

1089.复写零

[力扣](https://leetcode-cn.com/problems/duplicate-zeros/)

题目要求将数组中的0重写一遍，并保留最后的前len(arr)个数，那么我们可以先从左向右一趟扫描，记录下过程中有几个0被重写了，记为zero_cnt，同时记录下新数组的最后一个数在原数组中的下标，记为cut_pos。

接下来从cut_pos开始向前遍历，对于当前的arr[index]，其在新数组中的位置就应该是index + zero_cnt。若当前arr[index]为0，则需要将其重复一次，即将arr[index + zero_cnt - 1]也填上0，同时将zero_cnt减去1。

需要注意一种特殊情况是新数组的最后一个数为0，但这个0不是被重写的。

举个例子，[1, 0, 2, 0, 3]，重写后应该是[1, 0, 0, 2, 0, 0, 3]，那么答案就是[1, 0, 0, 2, 0]，其中第2个0此时没有被重写过。

于是可以使用一个标记表示答案的最后一个0是否是被重写过的，若不是，那么在从cut_pos向前扫描时，就应当将这个0视为非0的数字不进行重写操作。

最后附上python代码：

```python
class Solution(object):
    def duplicateZeros(self, arr):
        """
        :type arr: List[int]
        :rtype: None Do not return anything, modify arr in-place instead.
        """

        zero_cnt = 0
        ignore_last = False
        for cut_pos in range(len(arr)):
            if zero_cnt + cut_pos == len(arr) - 1:
                if arr[cut_pos] == 0:
                    ignore_last = True
                break
            if arr[cut_pos] == 0:
                zero_cnt += 1
                if zero_cnt + cut_pos == len(arr) - 1:
                    break

        for index in range(cut_pos, -1, -1):
            arr[index + zero_cnt] = arr[index]
            if arr[index] == 0:
                if ignore_last:
                    ignore_last = False
                else:
                    arr[index + zero_cnt - 1] = arr[index]
                    zero_cnt -= 1
```
