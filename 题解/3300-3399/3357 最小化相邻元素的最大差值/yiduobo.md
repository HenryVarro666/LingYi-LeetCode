---
title: "3357. 最小化相邻元素的最大差值"
aliases: ["yiduobo的每日leetcode 3357.最小化相邻元素的最大差值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/27163984416"
zhihu_id: "27163984416"
zhihu_title: "yiduobo的每日leetcode 3357.最小化相邻元素的最大差值"
question_id: "3357"
question: "最小化相邻元素的最大差值"
problem_url: "https://leetcode.cn/problems/minimize-the-maximum-adjacent-element-difference/"
difficulty: "Hard"
rating: 3077
created: "2025-02-28T23:32:01+08:00"
updated: "2025-02-28T23:32:01+08:00"
upvotes: 2
comments: 0
---

# 3357. 最小化相邻元素的最大差值

> **[yiduobo的每日leetcode 3357.最小化相邻元素的最大差值](https://zhuanlan.zhihu.com/p/27163984416) · 知乎 · 2025-02-28 · 赞同 2**
> 力扣：[3357. 最小化相邻元素的最大差值](https://leetcode.cn/problems/minimize-the-maximum-adjacent-element-difference/) · Hard · 灵茶山艾府：[O(n) 贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3357.最小化相邻元素的最大差值

[3357. 最小化相邻元素的最大差值 - 力扣（LeetCode）](https://leetcode.cn/problems/minimize-the-maximum-adjacent-element-difference/)

题目中给出一个整数数组nums，其中有一些缺失的元素，被标记为-1。现在要求选择一个正整数对(x, y)，将nums中的所有-1都替换成x或y。问如何替换才能使得替换后的nums中，相邻元素绝对差值的最大值最小。

对于这类使得最大值最小的问题，一种场景的处理方法就是二分答案。具体来说，就是二分这个最大差值，然后检测能否得到一种可行的构造方案。

不妨设nums中与-1相邻的最大值为ma，与-1相邻的最小值为mi，且当前二分到mid，那么在这里就应该令x为mi + mid，令y为ma - mid，这样一来x和y才有可能覆盖住尽量多的元素。

接下来尝试构造。nums与-1相关的情况可以分为：

1、与单个-1相邻的元素，可以是前缀、后缀、或者两个元素中间夹住了单个-1

对于这类情况，只需检测x或y填充到这个相邻的-1时是否合法

2、两个元素之间夹住多个-1

除了全部填充x或全部填充y之外，还可以前半段-1填充x，后半段-1填充y，或者反过来前半段填充y，后半段填充x。只需检测这四种填充方案是否至少有一种合法

具体实现上，可以使用两个指针p和q从nums头部开始向后遍历，先找出下一个-1的nums[p]，然后找出p后的第一个非-1的元素nums[q]，若p和q相邻，那么就属于上面的情况1，否则属于情况2。

另外对于二分的初始上界，自然就是ma - mi，而下界则应该取nums中相邻非-1元素的绝对差最大值。

最后附上python代码：

```python
class Solution(object):
    def minDifference(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        ma = None
        mi = None
        left = 0
        right = 0

        for index, v in enumerate(nums):
            if v == -1:
                if index > 0 and nums[index - 1] != -1:
                    if ma is None or ma < nums[index - 1]:
                        ma = nums[index - 1]
                    if mi is None or mi > nums[index - 1]:
                        mi = nums[index - 1]
                if index + 1 < n and nums[index + 1] != -1:
                    if ma is None or ma < nums[index + 1]:
                        ma = nums[index + 1]
                    if mi is None or mi > nums[index + 1]:
                        mi = nums[index + 1]
            else:
                if index > 0 and nums[index - 1] != -1:
                    left = max(left, abs(nums[index] - nums[index - 1]))
                if index + 1 < n and nums[index + 1] != -1:
                    left = max(left, abs(nums[index] - nums[index + 1]))
        
        if ma is not None:
            right = ma - mi
            while left < right:
                mid = (left + right) // 2
                x = mi + mid
                y = ma - mid
                flag = True

                p = 0
                while p < n:
                    while p < n and nums[p] != -1:
                        p += 1
                    
                    if p == n:
                        break
                    
                    q = p + 1
                    while q < n and nums[q] == -1:
                        q += 1
                    
                    if p + 1 == q:
                        if ((p > 0 and abs(x - nums[p - 1]) > mid) or (q < n and abs(x - nums[q]) > mid)) and \
                            ((p > 0 and abs(y - nums[p - 1]) > mid) or (q < n and abs(y - nums[q]) > mid)):
                            flag = False
                            break
                    else:
                        if ((p > 0 and abs(x - nums[p - 1]) > mid) or (q < n and abs(x - nums[q]) > mid)) and \
                            ((p > 0 and abs(y - nums[p - 1]) > mid) or (q < n and abs(y - nums[q]) > mid)) and \
                            ((p > 0 and abs(x - nums[p - 1]) > mid) or (q < n and abs(y - nums[q]) > mid) or abs(x - y) > mid) and \
                            ((p > 0 and abs(y - nums[p - 1]) > mid) or (q < n and abs(x - nums[q]) > mid) or abs(x - y) > mid):
                            flag = False
                            break

                    p = q + 1

                if flag:
                    right = mid
                else:
                    left = mid + 1
        
        return left
```
