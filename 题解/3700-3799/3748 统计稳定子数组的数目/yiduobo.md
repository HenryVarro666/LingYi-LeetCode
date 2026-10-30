---
title: "3748. 统计稳定子数组的数目"
aliases: ["yiduobo的每日leetcode 3748.统计稳定子数组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1973442129398362809"
zhihu_id: "1973442129398362809"
zhihu_title: "yiduobo的每日leetcode 3748.统计稳定子数组的数目"
question_id: "3748"
question: "统计稳定子数组的数目"
problem_url: "https://leetcode.cn/problems/count-stable-subarrays/"
difficulty: "Hard"
rating: 2209
created: "2025-11-17T20:03:54+08:00"
updated: "2025-11-17T20:03:55+08:00"
upvotes: 2
comments: 0
---

# 3748. 统计稳定子数组的数目

> **[yiduobo的每日leetcode 3748.统计稳定子数组的数目](https://zhuanlan.zhihu.com/p/1973442129398362809) · 知乎 · 2025-11-17 · 赞同 2**
> 力扣：[3748. 统计稳定子数组的数目](https://leetcode.cn/problems/count-stable-subarrays/) · Hard · 灵茶山艾府：[两种方法：二分查找 / 记录下一个递增段的左端点，附进阶问题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3748.统计稳定子数组的数目

[3748. 统计稳定子数组的数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-stable-subarrays/description/)

题目给出一个整数数组nums。

对于nums中的一个子数组，若其中没有逆序对，即不存在一组下标i和j，满足i \< j且nums[i] > nums[j]，那么就称该子数组为稳定子数组。

另外给出一个长度为q的二维整数数组queries，对于其中的每一组询问[left, right]，要求计算在nums[left: right + 1]中稳定子数组的数目。

题目中的稳定子数组实际上就是单调不减的子数组，于是可以先一趟遍历，尽可能长地分离出nums中所有的单调不减子数组，不妨将这些子数组记为parts，其中parts\[index\] \= \[start\[index\], end\[index\]\]，表示nums\[start\[index\]\]到nums\[end\[index\]\]这一段形成了一个尽可能长的单调不减子数组。

可以明确的是，任意单调不减子数组只会出现在parts中的某个子数组的内部，而不会跨越两个parts，因为根据parts的定义，任意两个相邻parts交界处的元素对是逆序的。

另一方面，对于parts\[index\] \= \[start\[index\], end\[index\]\]，其长度length为end\[index\] - start\[index\] + 1，那么其中就一共有length个长度为1的稳定子数组、length - 1个长度为2的稳定子数组、...、1个长度为length的稳定子数组，因此其中一共有(1 + length) \* length // 2个稳定子数组。

方便起见，接下来记cnt(length)为(1 + length) \* length // 2，也就是用cnt(length)表示长度为length的数组中子数组的个数。

接下来对于一组查询[left, right]，可以在最开始预处理parts的时顺带记录每个元素属于哪个parts，不妨记为belong，其中belong[index]表示nums[index]属于哪个parts，那么：

1、若belong[left]与belong[right]相同：

说明查询的子数组nums[left: right + 1]中的所有元素都位于同一个parts，此时nums[left: right + 1]中的任意子数组都是稳定的，因此对应的答案就是cnt(right - left + 1)

2、若belong[left]与belong[right]不同：

由于稳定子数组不会跨越parts，因此此时的答案可以分为三个部分进行考虑，分别为

2-1）parts\[belong\[left\]\]中，left到parts\[belong\[left\]\]的末尾，也就是nums\[left\]到nums\[parts\[belong\[left\]\]\[1\]\]这一段中的任意子数组。其中稳定子数组的数量为cnt(parts\[belong\[left\]\]\[1\] - left + 1)。

2-2）parts\[belong\[right\]\]中，parts\[belong\[right\]\]的开头到right，也就是nums\[parts\[belong\[right\]\]\[0\]\]到nums\[right\]这一段中的任意子数组。其中稳定子数组的数量为cnt(right - parts\[belong\[right\]\]\[0\] + 1)。

2-3）parts\[belong\[left\] + 1\]、parts\[belong\[left\] + 2\]、...、parts\[belong\[right\] - 1\]\]这些parts中各自的全部子数组。可以发现，这是一个区间和的形式，可以将其转化为前缀和之差进行求解。

使用数组s记录每个parts中子数组数目的前缀和，方便期间，记s\[0\] \= 0，那么在一开始分离parts时，对于新分离出的parts\[index\] \= \[start\[index\], end\[index\]\]，就可以顺便计算其中子数组的数目cnt(end\[index\] - start\[index\] + 1)，然后将其与s\[-1\]累加后，添加到s的末尾。

这样一来，第三部分的子数组数目就是parts\[0\]到parts\[belong\[right\] - 1\]的子数组数目之和，减去parts\[0\]到parts\[belong\[left\]\]的子数组数目之和，即s\[belong\[right\]\] - s\[belong\[left\] + 1\]。

需要注意这里不是s\[belong\[right\] - 1\]\] - s\[belong\[left\]\]，理由是一开始设置了s\[0\] \= 0，因此s数组的下标有1的偏移。

这样一来，就可以通过O(n)的预处理得到parts、belong以及s，然后对于每组查询，都可以在O(1)的时间内计算出对应的结果了。

最后附上python代码：

```python
class Solution(object):
    def countStableSubarrays(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        def cnt(length):
            return (1 + length) * length // 2

        parts = []
        p = 0
        s = [0]
        belong = [None] * len(nums)
        while p < len(nums):
            belong[p] = len(parts)
            q = p + 1
            while q < len(nums) and nums[q] >= nums[q - 1]:
                belong[q] = len(parts)
                q += 1
            
            parts.append((p, q - 1))
            s.append(s[-1] + cnt(q - p))
            p = q
        
        res = []
        for x, y in queries:
            if belong[x] == belong[y]:
                res.append(cnt(y - x + 1))
            else:
                res.append(cnt(parts[belong[x]][1] - x + 1) + cnt(y - parts[belong[y]][0] + 1) + s[belong[y]] - s[belong[x] + 1])
        
        return res
```
