---
title: "3006. 找出数组中的美丽下标I & 3008. 找出数组中的美丽下标II"
aliases: ["yiduobo的每日leetcode 3006.找出数组中的美丽下标I && 3008.找出数组中的美丽下标II", "3006. 找出数组中的美丽下标I", "3008. 找出数组中的美丽下标II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/binary-search", "leetcode/string-matching", "leetcode/hard", "题单/字符串", "题单/字符串/一-KMP-前缀的后缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/693651939"
zhihu_id: "693651939"
zhihu_title: "yiduobo的每日leetcode 3006.找出数组中的美丽下标I && 3008.找出数组中的美丽下标II"
question_id: ["3006", "3008"]
question: ["找出数组中的美丽下标 I", "找出数组中的美丽下标 II"]
problem_url: ["https://leetcode.cn/problems/find-beautiful-indices-in-the-given-array-i/", "https://leetcode.cn/problems/find-beautiful-indices-in-the-given-array-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2016
created: "2024-04-21T03:11:46+08:00"
updated: "2024-04-21T03:11:46+08:00"
upvotes: 1
comments: 0
---

# 3006. 找出数组中的美丽下标I & 3008. 找出数组中的美丽下标II

> **[yiduobo的每日leetcode 3006.找出数组中的美丽下标I && 3008.找出数组中的美丽下标II](https://zhuanlan.zhihu.com/p/693651939) · 知乎 · 2024-04-21 · 赞同 1**
> 力扣：[3006. 找出数组中的美丽下标 I](https://leetcode.cn/problems/find-beautiful-indices-in-the-given-array-i/) · Medium · 灵茶山艾府：[两种非暴力做法：KMP+二分查找/双指针（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3008. 找出数组中的美丽下标 II](https://leetcode.cn/problems/find-beautiful-indices-in-the-given-array-ii/) · Hard · 灵茶山艾府：[两种写法：KMP+二分查找/双指针（Python/Java/C++/Go）](../3008%20找出数组中的美丽下标%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3006.找出数组中的美丽下标I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-beautiful-indices-in-the-given-array-i/description/)

3008.找出数组中的美丽下标II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-beautiful-indices-in-the-given-array-ii/description/)

题目给出三个字符串s、a、b以及一个整数，要求对于a在s中出现的所有起点下标以及b在s中出现的所有起点下标，若对于某个a的起点i，存在某个b的起点j与i的距离小于等于k，那么就将i加入到答案中。

两个题目要做的事情是一样的，第二题中的数据规模相比较大。

由于要找出a和b在s中出现的所有起点下标，且字符串的长度都比较大，那么在这里就需要对a和b分别计算next数组，然后利用kmp算法找出a和b在s中出现的所有起点下标。

记a的所有起点下标数组为match_a，b的所有起点下标数组为match_b，那么对于某个a的起点match_a[p]，只需要用离match_a[p]最近的两个b的起点与之对比，分别是小于等于i的最大的下标match_b[q]，以及大于i的最小的下标match_b[q + 1]。于是只需从左向右一趟遍历a的起点match_a[p]，那么match_b[q]也会随着match_a[p]单调不减，因此在这里利用单调性就可以在均摊O(1)的时间内找出match_b[q]，接下来比对下标间的距离即可。

最后附上python代码：

```python
class Solution(object):
    def beautifulIndices(self, s, a, b, k):
        """
        :type s: str
        :type a: str
        :type b: str
        :type k: int
        :rtype: List[int]
        """

        def get_nxt(t):
            f = [0]
            p = 0
            for index in range(1, len(t)):
                while p and t[p] != t[index]:
                    p = f[p - 1]
                
                if t[p] == t[index]:
                    p += 1
                
                f.append(p)
            
            return f

        nxt_a = get_nxt(a)
        nxt_b = get_nxt(b)

        p = q = 0
        match_a = []
        match_b = [-k - 1]

        for index in range(len(s)):
            while p and a[p] != s[index]:
                p = nxt_a[p - 1]
            if a[p] == s[index]:
                p += 1
                if p == len(a):
                    match_a.append(index - p + 1)
                    p = nxt_a[p - 1]
            
            while q and b[q] != s[index]:
                q = nxt_b[q - 1]
            if b[q] == s[index]:
                q += 1
                if q == len(b):
                    match_b.append(index - q + 1)
                    q = nxt_b[q - 1]
        
        
        p = q = 0
        res = []
        while p < len(match_a):
            while q + 1 < len(match_b) and match_b[q + 1] <= match_a[p]:
                q += 1
            
            if q != 0 and match_a[p] - match_b[q] <= k:
                res.append(match_a[p])
            elif q + 1 < len(match_b) and match_b[q + 1] - match_a[p] <= k:
                res.append(match_a[p])

            p += 1
            
        
        return res
```
