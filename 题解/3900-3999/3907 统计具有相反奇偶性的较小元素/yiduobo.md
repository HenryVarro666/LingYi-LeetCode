---
title: "3907. 统计具有相反奇偶性的较小元素"
aliases: ["yiduobo的每日leetcode 3907.统计具有相反奇偶性的较小元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2031839898240557619"
zhihu_id: "2031839898240557619"
zhihu_title: "yiduobo的每日leetcode 3907.统计具有相反奇偶性的较小元素"
question_id: "3907"
question: "统计具有相反奇偶性的较小元素"
problem_url: "https://leetcode.cn/problems/count-smaller-elements-with-opposite-parity/"
created: "2026-04-26T21:26:29+08:00"
updated: "2026-04-26T21:26:32+08:00"
upvotes: 1
comments: 0
---

# 3907. 统计具有相反奇偶性的较小元素

> **[yiduobo的每日leetcode 3907.统计具有相反奇偶性的较小元素](https://zhuanlan.zhihu.com/p/2031839898240557619) · 知乎 · 2026-04-26 · 赞同 1**
> 力扣：[3907. 统计具有相反奇偶性的较小元素](https://leetcode.cn/problems/count-smaller-elements-with-opposite-parity/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3907.统计具有相反奇偶性的较小元素

<https://leetcode.cn/problems/count-smaller-elements-with-opposite-parity/description/>

题目给出一个长度为n的整数数组nums。

对于一组下标(i, j)，若满足：

- i \< j \< n
- nums[j] \< nums[i]
- nums[i]和nums[j]不同奇偶

那么下标i就可以得到一分。

现在要求返回一个长度为n的数组answer，表示每个下标的得分是多少。

如果不考虑奇偶性的限制，题目实际上就是要求计算数组中每个元素与其右侧元素形成的逆序对的数量。对于逆序对问题的求解，可以通过分治法，在归并排序的过程中顺便计算。

具体来说，对于一段子数组[left, right]，先计算中点mid \= (left + right) // 2，然后递归求解[left, mid]和[mid + 1, right]中的逆序对，这样一来，left到mid这一段和mid + 1到right这一段就都是单调不减的了。接下来对这两段执行二路归并，若当前是左侧的元素较小，那么就说明剩下的右侧元素都比它大，而之前已经归并进去的右侧元素都比它小，因此之前有多少个处理完的右侧元素，就可以形成多少个逆序对。

而对于本题，在常规逆序对的基础上，还需要考虑奇偶性的问题，因此在二路归并时，需要分别计算已经归并进去的右侧元素中奇数和偶数的数量odd以及even，那么若当前的左侧元素较小，则可以根据其奇偶性计算合法逆序对的数量了，即若当前元素为偶数，那么其与右侧已经归并进去的奇数形成逆序对，一共odd个，反之则可以与偶数形成逆序对，一共even个。反之，若当前右侧元素较小，则只需根据其奇偶性更新odd或者even即可。

需要特别注意的是，本题需要计算的是每个元素与后方元素形成的逆序对数量，因此在递归计算时需要携带这些元素的原始下标，方便更新答案。

最后附上python代码：

```python
class Solution(object):
    def countSmallerOppositeParity(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        n = len(nums)
        res = [0] * n
        arr = [(v, index) for index, v in enumerate(nums)]

        def calc(arr, left, right, res):
            if left == right:
                return

            mid = (left + right) // 2
            calc(arr, left, mid, res)
            calc(arr, mid + 1, right, res)

            odd, even = 0, 0
            i, j = left, mid + 1
            tmp = []
            while i <= mid or j <= right:
                if i == mid + 1:
                    tmp.append(arr[j])
                    j += 1
                elif j == right + 1 or arr[i][0] <= arr[j][0]:
                    if arr[i][0] % 2 == 0:
                        res[arr[i][1]] += odd
                    else:
                        res[arr[i][1]] += even
                    tmp.append(arr[i])
                    i += 1
                else:
                    tmp.append(arr[j])
                    if arr[j][0] % 2 == 0:
                        even += 1
                    else:
                        odd += 1
                    j += 1
            
            for index in range(left, right + 1):
                arr[index] = tmp[index - left]
        
        calc(arr, 0, n - 1, res)
        return res
```
