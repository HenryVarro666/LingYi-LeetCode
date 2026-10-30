---
title: "2023. 连接后等于目标字符串的字符串对"
aliases: ["yiduobo的每日leetcode 2023.连接后等于目标字符串的字符串对"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/string", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/506963126"
zhihu_id: "506963126"
zhihu_title: "yiduobo的每日leetcode 2023.连接后等于目标字符串的字符串对"
question_id: "2023"
question: "连接后等于目标字符串的字符串对"
problem_url: "https://leetcode.cn/problems/number-of-pairs-of-strings-with-concatenation-equal-to-target/"
difficulty: "Medium"
created: "2022-04-29T02:28:49+08:00"
updated: "2022-04-29T02:28:49+08:00"
upvotes: 0
comments: 0
---

# 2023. 连接后等于目标字符串的字符串对

> **[yiduobo的每日leetcode 2023.连接后等于目标字符串的字符串对](https://zhuanlan.zhihu.com/p/506963126) · 知乎 · 2022-04-29 · 赞同 0**
> 力扣：[2023. 连接后等于目标字符串的字符串对](https://leetcode.cn/problems/number-of-pairs-of-strings-with-concatenation-equal-to-target/) · Medium · 灵茶山艾府：[哈希表做法：枚举前缀+后缀](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2023.连接后等于目标字符串的字符串对

[力扣](https://leetcode-cn.com/problems/number-of-pairs-of-strings-with-concatenation-equal-to-target/)

题目要求找出所有的字符串对数目，要求两个字符串拼接后恰好与目标字符串一致。

直接枚举字符串对，拼接后与target比较是可行的做法，时间复杂度为O(n^2 \* l)，算是勉强过关。当然，也有不少优化的余地。

首先，对于拼接后字符串是否等于target的判断，可以分成两部分来看，即前半部分的字符串能与target的前缀匹配，以及后半部分的字符串能与target的后缀匹配。除了前半部分以及后半部分必须都与target匹配外，还需要满足这两个部分长度之和恰好等于target的长度。

对于上面这个问题，可以拆成两个部分：

1、首先找出nums中能与target前缀匹配的字符串，并使用一个标记数组记录下来。同样的，还需要找出nums中与target后缀匹配的字符串，同样使用标记数组记录。对于这个问题，由于需要遍历nums中的每个字符串，因此处理这个问题的时间复杂度下限就是朴素算法的复杂度，为O(nl)

2、接下来对于能与前后缀匹配的字符串中，需要找出所有长度和恰好为target长度的字符串对，且两个字符串的对应的标记都为真。对于这个问题，朴素的枚举算法时间复杂度为O(n^2)。当然，在这里也可以利用单调性，即前半部分的长度增加时，后半部分的长度必然要减小，因此可以将每种可以匹配前缀或者后缀的字符串出现的次数统计出来，然后使用类似两数之和的做法，排序后使用双指针来进行计算。在这里需要注意的是，如果使用双指针，就需要去重同一个字符串重复两次得到target这种情况。

我在这里偷懒，使用的是朴素的枚举算法。

最后附上python代码：

```python
class Solution(object):
    def numOfPairs(self, nums, target):
        """
        :type nums: List[str]
        :type target: str
        :rtype: int
        """

        n = len(nums)
        left_flag = []
        right_flag = []
        num_l = []
        target_l = len(target)

        for num in nums:
            num_l.append(len(num))
            if num_l[-1] >= target_l:
                left_flag.append(False)
                right_flag.append(False)
                continue
            
            flag = True
            for index in range(num_l[-1]):
                if num[index] != target[index]:
                    flag = False
                    break
            left_flag.append(flag)

            flag = True
            for index in range(num_l[-1]):
                if num[-index - 1] != target[-index - 1]:
                    flag = False
                    break
            right_flag.append(flag)
        
        res = 0
        for left in range(n):
            for right in range(n):
                if left == right:
                    continue
                if num_l[left] + num_l[right] == target_l and left_flag[left] and right_flag[right]:
                    res += 1
        
        return res
```
