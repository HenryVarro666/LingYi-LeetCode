---
title: "3261. 统计满足K约束的子字符串数量II"
aliases: ["yiduobo的每日leetcode 3261.统计满足K约束的子字符串数量II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/two-pointers", "leetcode/binary-search", "leetcode/prefix-sum", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/731169285"
zhihu_id: "731169285"
zhihu_title: "yiduobo的每日leetcode 3261.统计满足K约束的子字符串数量II"
question_id: "3261"
question: "统计满足 K 约束的子字符串数量 II"
problem_url: "https://leetcode.cn/problems/count-substrings-that-satisfy-k-constraint-ii/"
difficulty: "Hard"
rating: 2659
created: "2024-09-27T01:21:07+08:00"
updated: "2024-09-27T01:21:07+08:00"
upvotes: 0
comments: 0
---

# 3261. 统计满足K约束的子字符串数量II

> **[yiduobo的每日leetcode 3261.统计满足K约束的子字符串数量II](https://zhuanlan.zhihu.com/p/731169285) · 知乎 · 2024-09-27 · 赞同 0**
> 力扣：[3261. 统计满足 K 约束的子字符串数量 II](https://leetcode.cn/problems/count-substrings-that-satisfy-k-constraint-ii/) · Hard · 灵茶山艾府：[滑动窗口+前缀和+二分查找/双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3261.统计满足K约束的子字符串数量II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-substrings-that-satisfy-k-constraint-ii/description/)

题目给出一个二进制字符串s以及一个整数k，若某个二进制字符串中0的数量不超过k，或者1的数量不超过k，那么这个字符串就是一个k约束字符串。

接下来给出一个询问数组queries，其中queries\[i\] \= \[l\[i\], r\[i\]\]，要求计算所有起点和终点都在l\[i\]到r\[i\]之间的k约束字符串的数量。

本题是之前3258题的加强版，本题将询问特定区间内k约束字符串的数量，而且还是多次询问，那么直接逐个用滑动窗口来计算显然是不行的，需要进行优化。

不妨先回顾之前3258题的处理方法，使用滑动窗口，在一趟遍历后可以得到以每个下标index为右边界时最小的可行左边界p，在这里可以将这些左边界都收集起来，记为left_bound数组，其中left_bound[index]表示窗口以index为右边界时对应的左边界下标。

那么对于left_bound，因为是基于单调性使用变长滑动窗口计算出来的，因此其一定是单调不减的，这一点后续可以利用上来。

接下来回到本题。对于询问起点和终点都在start到end之间的k约束字符串的数量，可以基于终点end也就是右边界进行拆解，得到

所有起点大于等于start，终点等于start的k约束字符串数量

所有起点大于等于start，终点等于start + 1的k约束字符串数量

。。。

所有起点大于等于start，终点等于end的k约束字符串数量

计算上面这一系列问题的答案之和，就是询问[start, end]对应的答案。

那么对于所有终点等于index的k约束字符串数量，其起点可以是left_bound[index]到index之间的任意下标，此时又可以分为两种情况：

1、当left_bound[index] \<\= start时：

这种情况下起点的取值范围在start到index之间，一共就有index - start + 1种合法的子串

2、当left_bound[index] > start时：

这种情况下起点的取值范围在left_bound[index]到index之间，与start无关，一共就有index - left_bound[index] + 1种合法的子串

接下来就需要利用到left_bound的单调性了。由于left_bound[start]到left_bound[end]这一段是单调不减的，那么就可以找出一个分界点p，满足left_bound[start]到left_bound[p]都小于等于start，而left_bound[p + 1]到left_bound[end]都是大于start的。

对于p的求解则可以通过在left_bound[start]到left_bound[end]之间二分start的位置，在logn的时间内解决。

得到p之后，对于处于start到p之间的终点index，对应的left_bound[index]都小于等于start，因此可以形成的合法子串数目就是

(start - start + 1) + (start + 1 - start + 1) + ... + (p - start + 1) \= (p - start + 2) \* (p - start + 1) // 2

而对于处于p + 1到end之间的终点index，对应的left_bound[index]都大于start，因此可以形成的合法子串数目就是

(p + 1- left_bound[p + 1] + 1) + (p + 2 - left_bound[p + 2] + 1) + ... + (end - left_bound[end] + 1)

方便起见，在这里记录length[index] \= index - left_bound[index] + 1，那么上面的式子就可以写成

length[p + 1] + length[p + 2] + ... + length[end]

这是一个区间和问题，转化为前缀和之后就可以在O(1)的时间内求解了

到了这里，就得到了一种可行的算法：

1、首先使用变长滑动窗口过一遍s，对于每个下标index计算对应的左边界left_bound[index]，同时利用index - left_bound[index] + 1来更新length[index]。

2、得到length[index]后，一趟遍历计算length的前缀和数组sum_of_length。

3、接下来对于每组询问[start, end]，先在left_bound[start]到left_bound[end]之间通过二分查找找到最大的满足left_bound[p] \<\= start的下标p，根据上面得到的计算公式，分别为

(p - start + 2) \* (p - start + 1) // 2

以及

sum_of_length[end] - sum_of_length[p]

来计算终点位于start到p之间以及p + 1到end之间的合法子串的数量，相加后即为当前询问对应的答案。

最后附上python代码：

```python
class Solution(object):
    def countKConstraintSubstrings(self, s, k, queries):
        """
        :type s: str
        :type k: int
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        length = []
        left_bound = []

        p = 0
        one = 0
        zero = 0
        for index, char in enumerate(s):
            if char == '1':
                one += 1
            else:
                zero += 1
            
            while one > k and zero > k:
                if s[p] == '0':
                    zero -= 1
                else:
                    one -= 1
                p += 1
            
            left_bound.append(p)
            length.append(index - p + 1)

        sum_of_length = []
        for index in range(len(s)):
            if index == 0:
                sum_of_length.append(length[0])
            else:
                sum_of_length.append(sum_of_length[-1] + length[index])

        res = []
        for start, end in queries:
            left = start
            right = end
            while left < right:
                mid = (left + right + 1) // 2
                if left_bound[mid] >= start:
                    right = mid - 1
                else:
                    left = mid
                
            res.append(sum_of_length[end] - sum_of_length[left] + (1 + left - start + 1) * (left - start + 1) // 2)
        

        return res
```
