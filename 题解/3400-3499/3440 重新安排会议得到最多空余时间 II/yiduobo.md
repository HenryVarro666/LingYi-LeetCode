---
title: "3440. 重新安排会议得到最多空余时间II"
aliases: ["yiduobo的每日leetcode 3440.重新安排会议得到最多空余时间II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/enumeration", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1891683936486270948"
zhihu_id: "1891683936486270948"
zhihu_title: "yiduobo的每日leetcode 3440.重新安排会议得到最多空余时间II"
question_id: "3440"
question: "重新安排会议得到最多空余时间 II"
problem_url: "https://leetcode.cn/problems/reschedule-meetings-for-maximum-free-time-ii/"
difficulty: "Medium"
rating: 1998
created: "2025-04-05T04:27:26+08:00"
updated: "2025-04-05T04:27:26+08:00"
upvotes: 0
comments: 0
---

# 3440. 重新安排会议得到最多空余时间II

> **[yiduobo的每日leetcode 3440.重新安排会议得到最多空余时间II](https://zhuanlan.zhihu.com/p/1891683936486270948) · 知乎 · 2025-04-05 · 赞同 0**
> 力扣：[3440. 重新安排会议得到最多空余时间 II](https://leetcode.cn/problems/reschedule-meetings-for-maximum-free-time-ii/) · Medium · 灵茶山艾府：[维护前三大的空位+枚举+分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3440.重新安排会议得到最多空余时间II

[3440. 重新安排会议得到最多空余时间 II - 力扣（LeetCode）](https://leetcode.cn/problems/reschedule-meetings-for-maximum-free-time-ii/description/)

题目给出一个整数eventTime，表示一个活动的总时长。这个活动始于t \= 0，结束于t \= eventTime。另外给出两个长度为n的整数数组startTime和endTime，分别表示这次活动中n个时间没有重叠的会议，其中第index个会议为\[startTime\[index\], endTime\[index\]\]。

现在可以重新安排1个会议，安排的规则是将会议的时间平移，但是需要保证会议时长不会发生改变，会议也不能被安排到整个活动时间之外。

问重新安排会议后，两个相邻会议间最大的空余时间是多少。

本题的题设与上题类似，但是本题只能调整一个会议的时间，不过调整的会议可以任意插入到可以插入的空余时间内，所以处理方法和上题完全不同。

不妨考虑移动第index个会议，这个会议的时长

move_length \= endTime[index] - startTime[index]

而这个会议距离上一个会议的时间

left \= startTime[index] - endTime[index - 1]

距离下一个会议的时间

right \= startTime[index + 1] - endTime[index]

接下来对于当前会议，由两种移动的方案。

第一种是直接让其紧挨上一个或者下一个会议，这样相当于将left和right这两段空闲时间合并的，因此可以使用left + right来更新答案。

第二种则是选择将当前会议移动到另外两个会议之间，此时相当于空余出了left + move_length + right这一段时间，但是这个移动有个前提，也就是move_length必须可以插入到另外两个会议的空余时间之内。

于是可以先对所时间区间进行一趟遍历，计算出其中最大的三段空余时间first、second、third，这里需要计算前三大而不是最大的理由是left或者right可能就是前三大空余时间之一或者之二，那么此时移动move_length相当于是第一种移动方案而不是第二种。

得到first、second、third之后，若满足一下条件之一，就可以使用left + move_length + right来更新答案：

1、max(left, right) \< first，且move_length \<\= first：

这种情况下，left和right都不是最大的时间空余，因此可以将当前会议移动到first所在的空余时间内

2、min(left, right) \< second，且move_length \<\= second：

这种情况下，即使max(left, right)占据了first或second中的一个位置，但是另一个位置必然不是min(left, right)，因此必然有一个空余时间可以将当前会议移动过去

3、move_length \<\= third：

这种情况下有至少三段空余时间可以将当前会议移动过去，即使left和right占据了其中两段，依然还剩一段可以进行移动

在具体实现上，还需要处理第一个会议左侧的空余时间，以及最后一个会议右侧的空余时间，所以我使用一个变量pre记录上一个会议的结束时间，pre初始为0，这样就可以处理第一个会议左侧的空余时间。而对于最后一个会议右侧的空余时间，则可以新增一个[eventTime, eventTime]的区间到所有会议的末尾，那么在遍历到最后一个会议时就可以正常计算对应的right了。

最后附上python代码：

```python
class Solution(object):
    def maxFreeTime(self, eventTime, startTime, endTime):
        """
        :type eventTime: int
        :type startTime: List[int]
        :type endTime: List[int]
        :rtype: int
        """
        
        first, second, third = 0, 0, 0
        pre = 0
        
        for start, end in zip(startTime, endTime):
            length = start - pre
            if length > first:
                first, second, third = length, first, second
            elif length > second:
                second, third = length, second
            elif length > third:
                third = length
            pre = end
        
        length = eventTime - pre
        if length > first:
            first, second, third = length, first, second
        elif length > second:
            second, third = length, second
        elif length > third:
            third = length
        
        startTime.append(eventTime)
        endTime.append(eventTime)

        pre = 0
        res = 0
        for index in range(len(startTime) - 1):
            move_length = endTime[index] - startTime[index]
            left = startTime[index] - pre
            right = startTime[index + 1] - endTime[index]
            res = max(res, left + right)

            if max(left, right) < first and move_length <= first:
                res = max(res, left + right + move_length)
            elif min(left, right) < second and move_length <= second:
                res = max(res, left + right + move_length)
            elif move_length <= third:
                res = max(res, left + right + move_length)

            pre = endTime[index]

        return res
```
