---
title: "3943. 递增后的数对数量"
aliases: ["yiduobo的每日leetcode 3943.递增后的数对数量"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "题单/常用数据结构", "题单/常用数据结构/十一-根号算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2044230467348600536"
zhihu_id: "2044230467348600536"
zhihu_title: "yiduobo的每日leetcode 3943.递增后的数对数量"
question_id: "3943"
question: "递增后的数对数量"
problem_url: "https://leetcode.cn/problems/number-of-pairs-after-increment/"
difficulty: "Hard"
rating: 2410
created: "2026-05-31T02:00:15+08:00"
updated: "2026-05-31T02:00:15+08:00"
upvotes: 1
comments: 0
---

# 3943. 递增后的数对数量

> **[yiduobo的每日leetcode 3943.递增后的数对数量](https://zhuanlan.zhihu.com/p/2044230467348600536) · 知乎 · 2026-05-31 · 赞同 1**
> 力扣：[3943. 递增后的数对数量](https://leetcode.cn/problems/number-of-pairs-after-increment/) · Hard · 灵茶山艾府：[分块（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3943.递增后的数对数量

<https://leetcode.cn/problems/number-of-pairs-after-increment/description/>

题目给出两个整数数组nums1和nums2，以及一个二维整数数组queries。其中nums1的长度不超过5，nums2以及queries的长度不超过50000，另外nums1和nums2中的数值大小不超过50000，查询中的tot也不超过50000，同时保证nums2中的元素大小始终不超过2 \* 10^9。

对于每个queries[index]，都属于以下两种类型之一：

- [1, x, y, val]：表示将nums2中，下标x到y这一段的所有元素都加上val
- [2, tot]：计算满足nums1[p] + nums2[q] \=\= tot的数对(p, q)的数量。

返回一个数组answer，记录每个第二种查询的结果。

题目涉及到区间修改，还需要查询全局状态下，等于某个特定值的元素数量，使用树形结构并不是很好处理。不过好在本题中nums2的长度是不变的，因此在这里可以采用分块的思路进行处理。

具体来说，不妨设nums2的长度为m，那么令b \= sqrt(m)向上取整，接下来将nums2从左至右分成若干个长度为b的块，基于b的取值，块的数量k必然小于等于b。接下来，先遍历所有的块，计算每个块中每种元素出现的次数，得到一个长度为k的哈希表数组cnt，其中cnt[p][v]表示第p个块中，元素v出现的次数。

接下来对于queries[index]：

1、如果是修改操作：

先一趟遍历，找出包含x的块的下标p。这个过程的时间复杂度为O(k)。

接下来，将nums2中从x到min(y, (p + 1) \* b - 1)这一段的元素都加上val，同时更新cnt[p]。这个过程的时间复杂度为O(b)。

若这里的y \<\= (p + 1) \* b - 1，说明已经修改完了，可以继续处理下一个query了，否则就需要让p继续向后推进，直到找到包含y的块的下标p。在这个推进过程中，p将滑过中间所有完整的块，在这里就可以使用一个长度为k的数组delta来记录整块的修改值，在p移动的过程中将对应delta[p]加上val就行了。这个过程的时间复杂度为O(k)。

最后，将nums2中从p \* b到y这一段的元素都加上val，同时更新cnt[p]就行了。这个过程的时间复杂度为O(b)。

综合起来，修改操作的时间复杂度就是O(b + k)，相当于O(sqrt(m))。

2、如果是查询操作：

先遍历nums1，对于当前遍历到的v，现在需要检测nums2中有多少个元素恰好等于target \= tot - v。

在这里就可以遍历所有的块，对于当前块p，需要先消除掉没有下放的delta\[p\]的影响，即查找块中恰好等于target - delta\[p\]的元素数量，也就是cnt\[p\]\[target - delta\[p\]\]，将其累加到答案中即可。这一步的时间复杂度为O(k)，相当于O(sqrt(m))。

再结合nums1的长度n，查询操作的时间复杂度就是O(n \* sqrt(m))，这里的n非常小，可以视为常数，即O(sqrt(m))。

综合起来，总的时间复杂度就是O(q \* sqrt(m))。值得一提的是，如果n在大一点不能完全不略掉的话，在这里就可以先对queries进行一趟遍历，统计两种操作的次数q1以及q2，根据这两个元素来动态调整分块的大小，使得两种操作的总时间复杂度尽量接近从而达到最优。

最后附上python代码：

```python
class Solution(object):
    def numberOfPairs(self, nums1, nums2, queries):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        m = len(nums2)

        b = int(m ** 0.5) + 1

        cnt = []
        delta = []
        for start in range(0, m, b):
            cnt.append({})
            delta.append(0)
            for v in nums2[start : start + b]:
                cnt[-1][v] = cnt[-1].get(v, 0) + 1

        res = []
        for q in queries:
            if q[0] == 1:
                x, y, val = q[1:]
                p = 0
                while (p + 1) * b - 1 < x:
                    p += 1
                
                for index in range(x, min(y + 1, (p + 1) * b)):
                    cnt[p][nums2[index]] -= 1
                    nums2[index] += val
                    cnt[p][nums2[index]] = cnt[p].get(nums2[index], 0) + 1
                
                if y <= (p + 1) * b - 1:
                    continue

                p += 1
                while (p + 1) * b - 1 < y:
                    delta[p] += val
                    p += 1
                
                for index in range(p * b, y + 1):
                    cnt[p][nums2[index]] -= 1
                    nums2[index] += val
                    cnt[p][nums2[index]] = cnt[p].get(nums2[index], 0) + 1
            
            else:
                res.append(0)
                for v in nums1:
                    target = q[1] - v
                    for p in range(len(cnt)):
                        res[-1] += cnt[p].get(target - delta[p], 0)

        return res
```
