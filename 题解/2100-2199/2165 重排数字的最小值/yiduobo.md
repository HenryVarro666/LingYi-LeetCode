---
title: "2165. 重排数字的最小值"
aliases: ["yiduobo的每日leetcode 2165.重排数字的最小值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/533004000"
zhihu_id: "533004000"
zhihu_title: "yiduobo的每日leetcode 2165.重排数字的最小值"
question_id: "2165"
question: "重排数字的最小值"
problem_url: "https://leetcode.cn/problems/smallest-value-of-the-rearranged-number/"
difficulty: "Medium"
rating: 1362
created: "2022-06-23T23:41:11+08:00"
updated: "2022-06-23T23:41:11+08:00"
upvotes: 0
comments: 0
---

# 2165. 重排数字的最小值

> **[yiduobo的每日leetcode 2165.重排数字的最小值](https://zhuanlan.zhihu.com/p/533004000) · 知乎 · 2022-06-23 · 赞同 0**
> 力扣：[2165. 重排数字的最小值](https://leetcode.cn/problems/smallest-value-of-the-rearranged-number/) · Medium · 灵茶山艾府：[排序：正数从小到大，负数从大到小](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2165.重排数字的最小值

[力扣](https://leetcode.cn/problems/smallest-value-of-the-rearranged-number/)

题目中的n可正可负，正数的最小值就是绝对值最小，而负数的最小值则要求绝对值最大，因此需要分开讨论。

首先是n \= 0的情况。在这种情况下没有任何操作空间，答案就是0。

接下来n \< 0的情况。为了使得答案的绝对值最大，那么就应该将较大的数字放在高位上，于是只需将数字按从大到小的顺序排列就行了。

最后是n > 0的情况。与上面相反，为了使得答案的绝对值最小，那么就应该将较小的数字放在高位上，于是此时应该将数字按从小到大的顺序排列。需要注意的是，题目不允许前导0的出现，那么在排列完成后，需要找到首个不为0的数字，将这个数字与最高位上的数字进行交换就能保证没有前导0了。

最后附上python代码：

```python
class Solution(object):
    def smallestNumber(self, num):
        """
        :type num: int
        :rtype: int
        """

        if num == 0:
            return 0

        neg_flag = False
        if num < 0:
            neg_flag = True
            num = -num
        
        num_list = []
        while num:
            num_list.append(str(num % 10))
            num /= 10
        
        if neg_flag:
            return -int(''.join(sorted(num_list, reverse=True)))
        else:
            num_list = sorted(num_list)
            p = 0
            while num_list[p] == '0':
                p += 1
            num_list[0], num_list[p] = num_list[p], num_list[0]
            return int(''.join(num_list))
```
