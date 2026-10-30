---
title: "2380. 二进制字符串重新安排顺序需要的时间"
aliases: ["yiduobo的每日leetcode 2380.二进制字符串重新安排顺序需要的时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/dynamic-programming"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/564515226"
zhihu_id: "564515226"
zhihu_title: "yiduobo的每日leetcode 2380.二进制字符串重新安排顺序需要的时间"
question_id: "2380"
question: "二进制字符串重新安排顺序需要的时间"
problem_url: "https://leetcode.cn/problems/time-needed-to-rearrange-a-binary-string/"
difficulty: "Medium"
created: "2022-09-15T03:55:11+08:00"
updated: "2022-09-15T03:55:11+08:00"
upvotes: 0
comments: 0
---

# 2380. 二进制字符串重新安排顺序需要的时间

> **[yiduobo的每日leetcode 2380.二进制字符串重新安排顺序需要的时间](https://zhuanlan.zhihu.com/p/564515226) · 知乎 · 2022-09-15 · 赞同 0**
> 力扣：[2380. 二进制字符串重新安排顺序需要的时间](https://leetcode.cn/problems/time-needed-to-rearrange-a-binary-string/) · Medium · 灵茶山艾府：[O(n) 一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2380.二进制字符串重新安排顺序需要的时间

[力扣](https://leetcode.cn/problems/time-needed-to-rearrange-a-binary-string/)

题目的数据规模不大，直接模拟整个排序过程是可行的做法，不过题目最后也提出了存在一种O(n)的做法，那么就需要再考虑一下了。

根据题目给出的排序规则，结合样例可以发现，题目中的二进制字符串最终必然会将所有的1排到左侧，将所有的0排到右侧，那么在这里不妨考虑每个1归位需要的时间。

首先对于最左侧的1，归位的时间显然就是这个1左侧0的数目。

从左边起第二个1开始就有了一些变数。理想情况下，设这个1左侧有cnt个0，那么最短就可以在cnt的时间内完成所有需要进行的交换，但是存在一种情况是第二个1被第一个1卡住了，第一个样例就体现了这一点。

对于这种情况，第一个1会优先交换一次，此时就变成了101的形式。接下里的若干轮，这个101会一直维持不变直到第一个1被排到最左侧为止。最后，101会重新变为11。可以发现，这里第二个1归位所需的时间恰好等于第一个1所需时间再加上1。

更一般的，对于任意位置的两个连续1，可能有以下几种变化：

a、左侧1被卡住。此时11将保持不变，直到左侧1可以移动为止

b、左侧1可以移动，此时左侧1先交换，形成了101的形式。那么在左侧1再次被卡住之前，这两个1每一轮都可以进行交换，因此将一直保持101的形式不变，直到某一时刻左侧的1再次被卡住，此时右侧的1与中间的0进行交换，就会使得101再次变回到11

可以发现，对于任意位置的两个连续1，都会在重复若干次上面描述的过程后移动到目的地，也就是说，右侧1归位的时间恰好就等于左侧1归位的时间再加上1。

根据上面的结论，对于两个1而言，如果右侧的1在某一时刻可以与左侧的1凑在一起，那么右侧1归位所需的时间就等于左侧1归位所需的时间加上1。而如果右侧1一直没有与左侧的1凑在一起，说明右侧的1一直在进行交换，那么交换的次数就是其左侧0的数目。

于是就可以从左往右一趟遍历，使用变量cnt统计0出现的次数，res记录最后一个1归位所需的时间。对于每个1而言，其归位所需的时间就是前一个1归位所需时间res加上1，与cnt中的较大值，即res \= max(res + 1, cnt)

遍历完成后，最后一个1归位所需的时间，也就是当前的res就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def secondsToRemoveOccurrences(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        cnt = 0
        for char in s:
            if char == '0':
                cnt += 1
            elif cnt > 0:
                res = max(res + 1, cnt)
        
        return res
```
