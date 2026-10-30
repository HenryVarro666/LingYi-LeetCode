---
title: "2191. 将杂乱无章的数字排序"
aliases: ["yiduobo的每日leetcode 2191.将杂乱无章的数字排序"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/537144232"
zhihu_id: "537144232"
zhihu_title: "yiduobo的每日leetcode 2191.将杂乱无章的数字排序"
question_id: "2191"
question: "将杂乱无章的数字排序"
problem_url: "https://leetcode.cn/problems/sort-the-jumbled-numbers/"
created: "2022-07-04T01:31:18+08:00"
updated: "2022-07-04T01:31:18+08:00"
upvotes: 0
comments: 0
---

# 2191. 将杂乱无章的数字排序

> **[yiduobo的每日leetcode 2191.将杂乱无章的数字排序](https://zhuanlan.zhihu.com/p/537144232) · 知乎 · 2022-07-04 · 赞同 0**
> 力扣：[2191. 将杂乱无章的数字排序](https://leetcode.cn/problems/sort-the-jumbled-numbers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2191.将杂乱无章的数字排序

[力扣](https://leetcode.cn/problems/sort-the-jumbled-numbers/)

直接按照题目的描述进行模拟就行了。

首先对nums进行一趟遍历，将每个数字的数位都拆分出来，找到映射然后拼成映射后的数字。

接下来将下标0到n - 1进行排序，排序的主关键字为当前下标对应的映射后的数字，副关键字为当前下标自身。排序完成后，按当前的下标顺序将nums中的数依次填充到答案数组中即可。

最后附上python代码：

```python
class Solution(object):
    def sortJumbled(self, mapping, nums):
        """
        :type mapping: List[int]
        :type nums: List[int]
        :rtype: List[int]
        """

        mapped_nums = []
        for num in nums:
            digit_list = []
            while True:
                digit_list.append(mapping[num % 10])
                num /= 10
                if num == 0:
                    break
            
            for digit in digit_list[::-1]:
                num = num * 10 + digit
            
            mapped_nums.append(num)

        return [nums[index] for index in sorted(range(len(nums)), key=lambda d:(mapped_nums[d], d))]
```
