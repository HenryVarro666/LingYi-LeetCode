---
title: "2489. 固定比率的子字符串数"
aliases: ["yiduobo的每日leetcode 2489.固定比率的子字符串数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/632563528"
zhihu_id: "632563528"
zhihu_title: "yiduobo的每日leetcode 2489.固定比率的子字符串数"
question_id: "2489"
question: "固定比率的子字符串数"
problem_url: "https://leetcode.cn/problems/number-of-substrings-with-fixed-ratio/"
created: "2023-05-27T03:28:08+08:00"
updated: "2023-05-27T03:28:08+08:00"
upvotes: 0
comments: 0
---

# 2489. 固定比率的子字符串数

> **[yiduobo的每日leetcode 2489.固定比率的子字符串数](https://zhuanlan.zhihu.com/p/632563528) · 知乎 · 2023-05-27 · 赞同 0**
> 力扣：[2489. 固定比率的子字符串数](https://leetcode.cn/problems/number-of-substrings-with-fixed-ratio/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2489.固定比率的子字符串数

[力扣](https://leetcode.cn/problems/number-of-substrings-with-fixed-ratio/)

题目要求找出一个区间[left, right]，满足区间内0和1的比例为num1 : nums2。对于区间和问题，依然是采用经典处理方法，转化为前缀和来求解。

令zero[i]和one[i]分别表示前缀[0, i]之间0和1的数目，那么对于[left, right]，期间0和1的数目分别为zero[right] - zero[left - 1]以及one[right] - one[left - 1]，这二者之比如果是nums1 : nums2，那么就有

(zero[right] - zero[left - 1]) \* nums2 \= (one[right] - one[left - 1]) \* nums1

将left - 1和right项放到一起，就有

zero[right] \* nums2 - one[left] \* nums1 \= zero[left - 1] \* nums2 - one[left - 1] \* nums1

根据这个式就可以利用哈希表来求解。一趟遍历，一边计算前缀和数组zero和one，一边计算对应值v \= zero \* nums2 - one \* nums1。对于每个v，先查找其在哈希表出现的次数，并将这个次数累加到答案中，然后将v也加入到哈希表中。

具体实现时，由于zero和one都只与上一轮有关，且只需使用一次，因此可以使用变量迭代而不是数组。

最后附上python代码：

```python
class Solution(object):
    def fixedRatio(self, s, num1, num2):
        """
        :type s: str
        :type num1: int
        :type num2: int
        :rtype: int
        """

        cnt = {0 : 1}
        zero = one = 0
        res = 0
        for char in s:
            if char == '0':
                zero += 1
            else:
                one += 1
        
            v = zero * num2 - one * num1
            res += cnt.get(v, 0)
            cnt[v] = cnt.get(v, 0) + 1
        
        return res
```
