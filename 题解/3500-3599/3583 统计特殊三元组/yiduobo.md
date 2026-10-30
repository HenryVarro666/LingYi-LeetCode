---
title: "3583. 统计特殊三元组"
aliases: ["yiduobo的每日leetcode 3583.统计特殊三元组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "leetcode/combinatorics", "leetcode/enumeration", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/零-常用枚举技巧", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1938366321764046181"
zhihu_id: "1938366321764046181"
zhihu_title: "yiduobo的每日leetcode 3583.统计特殊三元组"
question_id: "3583"
question: "统计特殊三元组"
problem_url: "https://leetcode.cn/problems/count-special-triplets/"
difficulty: "Medium"
rating: 1510
created: "2025-08-11T22:39:59+08:00"
updated: "2025-08-11T22:39:59+08:00"
upvotes: 1
comments: 0
---

# 3583. 统计特殊三元组

> **[yiduobo的每日leetcode 3583.统计特殊三元组](https://zhuanlan.zhihu.com/p/1938366321764046181) · 知乎 · 2025-08-11 · 赞同 1**
> 力扣：[3583. 统计特殊三元组](https://leetcode.cn/problems/count-special-triplets/) · Medium · 灵茶山艾府：[两种方法：枚举中间 / 一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3583.统计特殊三元组

<https://leetcode.cn/problems/count-special-triplets/description/>

题目给出一个整数数组nums，定义特殊三元组为满足i \< j \< k的下标三元组，满足nums[i]和nums[k]都是nums[j]的两倍。问有多少个特殊三元组。

对于这类寻找三元组的问题，一种常见的思路是枚举正中间的下标j，然后分别检测0到j - 1这个前缀以及j + 1到n - 1这个后缀中有多少满足条件的i和k，然后将二者相乘后累加到答案中。

对于本题，则可以利用哈希表来判断合法i和k的数目。具体来说，先一趟遍历，使用一个全局哈希表total记录数组中每种元素出现的次数，然后在遍历j的过程中使用一个前缀哈希表prefix记录前缀中每种元素出现的次数。

对于当前遍历到的nums\[j\]，就可以使用prefix\[nums\[j\] \* 2\]获取下标0到下标j - 1中合法i的数目left，然后用total\[nums\[j\] \* 2\]减去前缀中合法i的数目即为下标j到下标n - 1中合法k的数目right。需要特别注意的是，若nums\[j\]为0，那么nums\[j\] \* 2也是0，而j到n - 1之间nums\[j\] \* 2的数目会将nums\[j\]也计算进去，因此在这里需要将right减去1。接下来，将left \* right累加到答案中，然后将prefix\[nums\[j\]\]加上1后继续向后遍历即可。

最后附上python代码：

```python
class Solution(object):
    def specialTriplets(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        total = {}
        for v in nums:
            total[v] = total.get(v, 0) + 1
        
        prefix = {}
        res = 0
        mod = 10 ** 9 + 7
        for v in nums:
            dv = v + v
            left = prefix.get(dv, 0)
            right = total.get(dv, 0) - left
            if v == dv:
                right -= 1
            
            res = (res + left * right) % mod
            prefix[v] = prefix.get(v, 0) + 1
        
        return res
```
