---
title: "3589. 计算质数间隔平衡子数组"
aliases: ["yiduobo的每日leetcode 3589.计算质数间隔平衡子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory", "leetcode/sliding-window", "leetcode/monotonic-queue", "题单/常用数据结构", "题单/常用数据结构/四-队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1939481237807935926"
zhihu_id: "1939481237807935926"
zhihu_title: "yiduobo的每日leetcode 3589.计算质数间隔平衡子数组"
question_id: "3589"
question: "计数质数间隔平衡子数组"
problem_url: "https://leetcode.cn/problems/count-prime-gap-balanced-subarrays/"
difficulty: "Medium"
rating: 2235
created: "2025-08-15T00:52:38+08:00"
updated: "2025-08-15T00:52:38+08:00"
upvotes: 1
comments: 0
---

# 3589. 计算质数间隔平衡子数组

> **[yiduobo的每日leetcode 3589.计算质数间隔平衡子数组](https://zhuanlan.zhihu.com/p/1939481237807935926) · 知乎 · 2025-08-15 · 赞同 1**
> 力扣：[3589. 计数质数间隔平衡子数组](https://leetcode.cn/problems/count-prime-gap-balanced-subarrays/) · Medium · 灵茶山艾府：[预处理质数+滑动窗口+单调队列（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3589.计算质数间隔平衡子数组

<https://leetcode.cn/problems/count-prime-gap-balanced-subarrays/description/>

题目给出一个整数数组nums和一个整数k，另外定义至少包含两个质数，且其中最大质数与最小质数之差小于等于k的子数组为质数间隔平衡子数组，问nums中质数间隔平衡子数组的数目。

对于数组中指定的下标index，若以index为子数组的左边界，那么子数组的右边界p越大，子数组中最大质数与最小质数之差就越大，也就是说在固定了左边界的情况下，越长的子数组越不可能是质数间隔平衡子数组。另一方面，当子数组的边界index与p固定时，若子数组为质数间隔平衡子数组，那么只要index + 1到p之间存在至少两个质数，那么index + 1到p的子数组也是质数平衡子数组。

基于上面的结论，就可以使用一个变长滑动窗口从左向右逐位滑动，每次左边界index向右滑动一步，同时更新最大的合法右边界p，那么以index为左边界时，可用的右边界就有从second[index]到p一共p - second[index] + 1个，其中second[index]表示从index起的第二个质数下标。

而对于最大的合法右边界p的求解，则可以视为滑动窗口最大/最小值问题，不过在这里只需要考虑窗口内的质数。对于这个问题，可以利用堆或者单调队列求解。我一开始使用的堆实现的，但是被卡了常数，后来又改成单调队列实现。

接下来说明如何使用单调队列求解滑动窗口最大值，求解最小值的方法类似：

对于滑动窗口中的两个下标x和y，若x \< y，那么y必然不会在x之前被移除出窗口，那么只要nums[y] > nums[x]，那么nums[x]就不可能成为滑动窗口的最大值了，因为窗口内始终存在nums[y]。基于这一点，就可以发现窗口内所有可能成为最大值的元素必然是随着下标单调递减的，因此在这里可以使用一个单调栈维护这些元素，当窗口右边界向后移动时，检测新加入的元素与队尾元素的大小，若新元素更大，那么就将队尾元素弹出，重复此过程直到队列为空或者队尾元素大于新加入的元素位置；当窗口左边界向后移动时，若移除的下标恰好是队首的下标，那么还需要将队首从队列中弹出。这样一来，就可以在均摊O(1)的时间内得到滑动窗口的最大值了。

对于本题，还有一个常数优化是由于本题决定p是否合法只取决于质数，那么就可以在最开始将nums中所有的质数都提取出来，形成二维数组prime_list，其中prime_list[index] \= [ori_index, v]，分别表示当前是数组中第index个质数，其原始下标为ori_index，其数值为v。

接下来，就只需要在prime_list上执行滑动窗口，找出每个index对应的最大的合法右边界p。

不过需要注意的是，此时找到的窗口中第一个质数下标为prime_list[index][0]，因此这个窗口左边界可以从prime_list[index - 1][0] + 1到prime_list[index][0]中任意选取，一共prime_list[index][0] - prime_list[index - 1][0]种。

同理，其右边界则可以从窗口内第二个质数的下标，也就是prime_list[index + 1][0]，到prime_list[p + 1][0] - 1之间选取，因为最后一个合法的质数下标是prime_list[p][0]，到prime_list[p + 1][0] - 1之间的这一段也是可以使用的，因此一共有prime_list[p + 1][0] - prime_list[index + 1][0]种。

二者相乘即为第一个质数下标为index的合法子数组数量。

最后附上python代码：

```python
class Solution(object):
    def primeSubarray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        prime = [None] * 50001
        for v in range(2, 50001):
            if prime[v] is None:
                prime[v] = True
                for x in range(v + v, 50001, v):
                    prime[x] = False
        
        prime_list = []
        for index, v in enumerate(nums):
            if prime[v]:
                prime_list.append((index, v))
        
        res = 0
        p = 0
        ma = deque()
        mi = deque()
        for index, (ori_index, v) in enumerate(prime_list):
            if p <= index:
                p = index + 1
                ma.append((ori_index, v))
                mi.append((ori_index, v))

            while p < len(prime_list) and abs(prime_list[p][1] - mi[0][1]) <= k and abs(ma[0][1] - prime_list[p][1]) <= k:
                while ma and ma[-1][1] <= prime_list[p][1]:
                    ma.pop()
                ma.append((prime_list[p][0], prime_list[p][1]))

                while mi and mi[-1][1] >= prime_list[p][1]:
                    mi.pop()
                mi.append((prime_list[p][0], prime_list[p][1]))
                
                p += 1
                

            if p - index > 1:
                if index == 0:
                    start_choice = ori_index + 1
                else:
                    start_choice = ori_index - prime_list[index - 1][0]
            
                if p == len(prime_list):
                    end_choice = len(nums) - prime_list[index + 1][0]
                else:
                    end_choice = prime_list[p][0] - prime_list[index + 1][0]

                res += start_choice * end_choice

            if ma and ma[0][0] == ori_index:
                ma.popleft()
            
            if mi and mi[0][0] == ori_index:
                mi.popleft()
        
        return res
```
