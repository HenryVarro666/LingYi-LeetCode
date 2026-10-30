---
title: "1534. 统计好三元组"
aliases: ["yiduobo的每日leetcode 1534.统计好三元组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/prefix-sum", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/423389947"
zhihu_id: "423389947"
zhihu_title: "yiduobo的每日leetcode 1534.统计好三元组"
question_id: "1534"
question: "统计好三元组"
problem_url: "https://leetcode.cn/problems/count-good-triplets/"
difficulty: "Easy"
created: "2021-10-20T00:03:16+08:00"
updated: "2021-10-20T00:05:32+08:00"
upvotes: 0
comments: 0
---

# 1534. 统计好三元组

> **[yiduobo的每日leetcode 1534.统计好三元组](https://zhuanlan.zhihu.com/p/423389947) · 知乎 · 2021-10-20 · 赞同 0**
> 力扣：[1534. 统计好三元组](https://leetcode.cn/problems/count-good-triplets/) · Easy · 灵茶山艾府：[三种方法：暴力枚举 / 前缀和 / 排序+三指针（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1534.统计好三元组

[力扣](https://leetcode-cn.com/problems/count-good-triplets/)

常规情况下对于这类三元组问题，经典的处理方法是枚举三元组中间的那个数，然后根据大小关系确定两侧的取值范围并储存，然后对于这些取值范围求解最终问题。

本题相对比较特殊，因为涉及到的大小关系是绝对值不等式，因此仅枚举中间的arr[j]还是不够的。在这里需要先枚举arr[j]，然后从0到j - 1之间枚举符合条件的arr[i]。接下来根据arr[i]与arr[k]的不等式以及arr[j]与arr[k]的不等式，可以求出arr[k]的取值范围。具体来说：

根据|arr[j] - arr[k]| \<\= b，就有-b \<\= arr[j] - arr[k] \<\= b，即

arr[j] - b \<\= arr[k] \<\= arr[j] + b

同理，根据|arr[i] - arr[k]| \<\= c可得

arr[i] - c \<\= arr[k] \<\= arr[i] + c

将枚举的arr[i]以及arr[j]带入上面的式子，就可以得到arr[k]最终的取值范围[l, r]，此时只需要检测arr[j + 1]到arr[n - 1]中大小处于l到r之间的数有多少即可。

此时问题转化成了一个动态区间和问题，但这个区间和比较特殊，是一个全加1的区间和，因此可以将其转化为前缀和，然后使用树状数组来进行求解。

最后附上python代码：

```python
class Solution(object):
    def countGoodTriplets(self, arr, a, b, c):
        """
        :type arr: List[int]
        :type a: int
        :type b: int
        :type c: int
        :rtype: int
        """

        suffix_array = [0] * 1002

        for num in arr:
            self.add(num + 1, 1001, suffix_array, 1)
        
        n = len(arr)
        res = 0
        for j in range(n):
            self.add(arr[j] + 1, 1001, suffix_array, -1)
            for i in range(j):
                if abs(arr[i] - arr[j]) <= a:
                    l1, r1 = max(arr[j] - b, 0) + 1, min(arr[j] + b, 1000) + 1
                    l2, r2 = max(arr[i] - c, 0) + 1, min(arr[i] + c, 1000) + 1
                    
                    l, r = max(l1, l2), min(r1, r2)
                    if l <= r:
                        res += self.sum(r, suffix_array)
                        if l > 0:
                            res -= self.sum(l - 1, suffix_array)
        
        return res
    
    def add(self, now, max_n, suffix_array, delta):
        while now <= max_n:
            suffix_array[now] += delta
            now += now & -now
    
    def sum(self, now, suffix_array):
        res = 0
        while now:
            res += suffix_array[now]
            now -= now & -now
        
        return res
```
