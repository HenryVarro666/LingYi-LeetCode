---
title: "3386. 按下时间最长的按钮"
aliases: ["yiduobo的每日leetcode 3386.按下时间最长的按钮"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/29578391974"
zhihu_id: "29578391974"
zhihu_title: "yiduobo的每日leetcode 3386.按下时间最长的按钮"
question_id: "3386"
question: "按下时间最长的按钮"
problem_url: "https://leetcode.cn/problems/button-with-longest-push-time/"
difficulty: "Easy"
created: "2025-03-12T00:10:10+08:00"
updated: "2025-03-12T00:10:21+08:00"
upvotes: 1
comments: 0
---

# 3386. 按下时间最长的按钮

> **[yiduobo的每日leetcode 3386.按下时间最长的按钮](https://zhuanlan.zhihu.com/p/29578391974) · 知乎 · 2025-03-12 · 赞同 1**
> 力扣：[3386. 按下时间最长的按钮](https://leetcode.cn/problems/button-with-longest-push-time/) · Easy · 灵茶山艾府：[一次遍历，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3386.按下时间最长的按钮

[3386. 按下时间最长的按钮 - 力扣（LeetCode）](https://leetcode.cn/problems/button-with-longest-push-time/)

题目给出一个二维数组events，表示孩子在键盘上按下一系列按钮触发的按钮事件。对于events\[i\] \= \[index\[i\], time\[i\]\]，表示在time\[i\]时按下了下标为index\[i\]的按钮。events按照time升序排列，且按下一个按钮所需的时间是连续两次按钮按下的时间差，其中按下第一个按钮所需的时间则为其时间戳。

问按下时间最长，且index最小的按钮是哪个。

首先对于events进行一趟遍历，使用当前的时间戳和上一个时间戳之差计算按下当前按钮的时间，并使用哈希表统计每种按钮按下的总时间。接下来对哈希表进行一趟遍历，取中其中按下时间最长，且编号最小的index作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def buttonWithLongestTime(self, events):
        """
        :type events: List[List[int]]
        :rtype: int
        """
        
        pre_index, pre_time = events[0]
        cnt = {pre_index: pre_time}
        for index, time in events[1:]:
            cnt[index] = max(cnt.get(index, 0), time - pre_time)
            pre_index, pre_time = index, time

        max_time = 0
        res = None
        for index in cnt:
            if cnt[index] > max_time or (cnt[index] == max_time and (res is None or res > index)):
                res = index
                max_time = cnt[index]
        return res
```
