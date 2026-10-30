---
title: "3690. 拆分合并数组"
aliases: ["yiduobo的每日leetcode 3690.拆分合并数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/breadth-first-search", "leetcode/hash-table", "leetcode/enumeration", "leetcode/shortest-path", "题单/位运算", "题单/图论算法", "题单/位运算/一-基础题", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1955349430136997827"
zhihu_id: "1955349430136997827"
zhihu_title: "yiduobo的每日leetcode 3690.拆分合并数组"
question_id: "3690"
question: "拆分合并数组"
problem_url: "https://leetcode.cn/problems/split-and-merge-array-transformation/"
difficulty: "Medium"
rating: 1982
created: "2025-09-29T21:35:06+08:00"
updated: "2025-09-29T21:35:08+08:00"
upvotes: 2
comments: 0
---

# 3690. 拆分合并数组

> **[yiduobo的每日leetcode 3690.拆分合并数组](https://zhuanlan.zhihu.com/p/1955349430136997827) · 知乎 · 2025-09-29 · 赞同 2**
> 力扣：[3690. 拆分合并数组](https://leetcode.cn/problems/split-and-merge-array-transformation/) · Medium · 灵茶山艾府：[BFS / 位运算优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3690.拆分合并数组

[3690. 拆分合并数组 - 力扣（LeetCode）](https://leetcode.cn/problems/split-and-merge-array-transformation/description/)

题目给出两个长度为n的整数数组nums1和nums2，n不超过6。现在可以对nums1执行任意次拆分合并操作，每次操作中，都需要：

1、选择一个子数组nums1[left: right + 1]

2、移除这个子数组，留下前缀nums1[:left]以及后缀nums1[right:]形成剩余数组

3、将移除的子数组重新插入到剩余数组的任意位置，也就是任意两个元素之间、最开始或者最末尾

问将nums1转换为nums2所需的最少操作次数。

首先可以明确的是，在每次操作后nums1中的元素没有凭空消失，也没有多出其他元素，也就是说得到的依然是nums1的某个排列。又由于nums1的长度n不超过6，因此最多只有6! \= 720中不同排列，在这里完全可以直接暴力bfs，计算从nums1变换到num2所需的最少操作次数。

对于当前的bfs队列中的now，先分别枚举left和right，然后取mid \= now[left: right]，然后将剩下的元素拼接成rest \= now[:left] + now[right:]。接下来从0到len(rest)枚举插入的位置index，得到的新数组就是rest[:index] + mid + rest[index:]，接下来只需检测这个新数组是否在之前遇到过，若没有，则将其加入到bfs队列中即可。

最后附上python代码：

```python
class Solution(object):
    def minSplitMerge(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """
        
        if nums1 == nums2:
            return 0
        
        q = [tuple(nums1)]
        head, tail = 0, 1
        res = 0
        n = len(nums1)
        vis = set(tuple(nums1))
        target = tuple(nums2)
        while head < tail:
            res += 1
            for now in q[head : tail]:
                for left in range(n):
                    for right in range(left, n):
                        if left == 0 and right == n - 1:
                            continue
                        
                        mid = now[left : right + 1]
                        rest = now[:left] + now[right + 1:]
                        for index in range(len(rest)):
                            nxt = rest[:index] + mid + rest[index:]
                            key = tuple(nxt)
                            if key not in vis:
                                vis.add(key)
                                q.append(key)
                                if target in vis:
                                    return res
            
            head, tail = tail, len(q)
        
        return 0
```
