---
title: "949. 给定数字能组成的最大时间"
aliases: ["yiduobo的每日leetcode 949.给定数字能组成的最大时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/359400945"
zhihu_id: "359400945"
zhihu_title: "yiduobo的每日leetcode 949.给定数字能组成的最大时间"
question_id: "949"
question: "给定数字能组成的最大时间"
problem_url: "https://leetcode.cn/problems/largest-time-for-given-digits/"
created: "2021-03-24T00:00:58+08:00"
updated: "2021-03-24T00:00:58+08:00"
upvotes: 0
comments: 0
---

# 949. 给定数字能组成的最大时间

> **[yiduobo的每日leetcode 949.给定数字能组成的最大时间](https://zhuanlan.zhihu.com/p/359400945) · 知乎 · 2021-03-24 · 赞同 0**
> 力扣：[949. 给定数字能组成的最大时间](https://leetcode.cn/problems/largest-time-for-given-digits/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

949.给定数组能组成的最大时间

[力扣](https://leetcode-cn.com/problems/largest-time-for-given-digits/)

由于只有4个数字，那么至多也就4！\= 24种排列，于是可以直接枚举每一种可能的排列，然后判断其是否合法并更新答案。

可以直接4重循环进行枚举，我这里采用的是dfs。

最后附上python代码：

```python
class Solution(object):
    def largestTimeFromDigits(self, arr):
        """
        :type arr: List[int]
        :rtype: str
        """

        self.res = ""
        self.minute = None
        used = [False] * 4
        self.dfs(arr, used, [])

        return self.res
    
    def dfs(self, arr, used, now):
        if len(now) == 4:
            if now[0] > 2:
                return
            if now[0] == 2 and now[1] > 3:
                return
            if now[2] > 5:
                return

            minute = (now[0] * 10 + now[1]) * 60 + now[2] * 10 + now[3]
            if self.minute is None or minute > self.minute:
                self.minute = minute
                self.res = str(now[0]) + str(now[1]) + ':' + str(now[2]) + str(now[3])
            
            return
        
        for index in range(4):
            if not used[index]:
                now.append(arr[index])
                used[index] = True
                self.dfs(arr, used, now)
                used[index] = False
                now.pop()
```
