---
title: "3480. 删除一个冲突对后最大子数组数目"
aliases: ["yiduobo的每日leetcode 3480.删除一个冲突对后最大子数组数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/enumeration", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1897275654870918699"
zhihu_id: "1897275654870918699"
zhihu_title: "yiduobo的每日leetcode 3480.删除一个冲突对后最大子数组数目"
question_id: "3480"
question: "删除一个冲突对后最大子数组数目"
problem_url: "https://leetcode.cn/problems/maximize-subarrays-after-removing-one-conflicting-pair/"
difficulty: "Hard"
rating: 2764
created: "2025-04-21T22:17:21+08:00"
updated: "2025-04-21T22:17:21+08:00"
upvotes: 2
comments: 0
---

# 3480. 删除一个冲突对后最大子数组数目

> **[yiduobo的每日leetcode 3480.删除一个冲突对后最大子数组数目](https://zhuanlan.zhihu.com/p/1897275654870918699) · 知乎 · 2025-04-21 · 赞同 2**
> 力扣：[3480. 删除一个冲突对后最大子数组数目](https://leetcode.cn/problems/maximize-subarrays-after-removing-one-conflicting-pair/) · Hard · 灵茶山艾府：[枚举左端点，维护最小次小 b（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3480.删除一个冲突对后最大子数组数目

[3480. 删除一个冲突对后最大子数组数目 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-subarrays-after-removing-one-conflicting-pair/description/)

题目给出一个整数n，表示一个包含从1到n按顺序排列的整数数组nums，n的取值范围可达10^5。另外给出一个二维数组conflictingPairs，其中conflictingPairs[index] \= [a, b]，表示a和b形成一个冲突对。

现在要求从conflictingPairs中删除恰好一个元素，然后计算nums中非空字数组的数目，这些字数组中不能包含任何剩下冲突对[a, b]中的a和b。

问删除一个冲突对后可能得到的最大子数组数目。

题目的数据规模比较大，直接暴力枚举所有的子数组显然是不行的。对于子数组计数相关的问题，一种经典的处理方法是枚举数组中的每个下标index，计算以index为右边界的合法子数组的数目，累加起来即为最终答案。对于本题，也可以通过这种方法求解。

---

简单起见，先不考虑从conflictingPairs中删除元素的话应该如何计算合法子数组的数目。

对于数组中的某个下标y，记f[y]为以y为右边界的合法子数组的最小合法左边界，那么在这里就可以形成nums[f[y] : y + 1]、nums[f[y] + 1 : y + 1]、...、nums[y : y + 1]这一共y - f[y] + 1个合法的子数组。接下来的问题就是如何计算这个f[y]。

首先，如果不存在任意冲突对，那么所有的子数组的左边界都可以设置为1，因此在这里可以先初始化所有的f[y]为1。接下来，对于conflictingPairs中所有的冲突对(x, y)，若x \< y，那么f[y]就必须大于x。那么对于所有满足x \< y的冲突对(x, y)，就有f[y] \= max(f[y], x + 1)。

然而，仅通过直接涉及到y的冲突对(x, y)是不足以得到f[y]的，例如样例1中的(2, 3)，(1, 4)，虽然涉及到4的冲突对只有(1, 4)，可以得到f[4] \= 1 + 1 \= 2，然而由于(2, 3)的存在，因此包含了3的子数组中是不能包含2的。以4为右边界的子数组中，如果左边界越过了3，那么就将3也包含进来了，此时的f[4]除了在原始的2之外，还需要额外考虑f[3]。更进一步的，应该有f[y] \= min(f[1], f[2], ..., f[y - 1])，也就是说出来直接通过(x, y)得来的f[y]之外，还需要考虑其左侧所有的f值。

这样一来，就可以先遍历conflictingPairs中所有的冲突对(x, y)，得到初步的f[y]，接下来再对f数组进行遍历，使用f[y] \= min(f[y], f[y - 1])来更新f数组。

得到f数组后，就可以上面提到的累加所有y - f[y] + 1得到最终答案了。

---

接下来再考虑删去一组冲突后可以得到的最大合法子数组数目。对于一组冲突(x, y)，还是设x \< y，那么在删去这一组冲突后，首先可能直接影响到f[y]的取值。更具体的，当f[y]恰好等于x时，那么在删去这一组冲突后，f[y]可能变得更小，这个更小的值可能来自f[y - 1]，也可能来自另一组以y结尾的冲突对(x', y)。那么在这里就可以将f[y]改写为两个数组first和second，其中first[y]还是保有原来f[y]的含义，而second[y]则表示不考虑冲突对(x, y)时可用的最大左边界。

对于first[y]和second[y]，首先还是通过conflictingPairs中的冲突对来进行更新，取其中所有满足x \< y的冲突对(x, y)中x的最大值和次大值，加1后作为初始的first[y]以及second[y]。接下来依然是从头开始向后一趟遍历，若first[y - 1] > first[y]，那么就将first[y]置为first[y - 1]，同时取first[y]和second[y - 1]中的较大值作为second[y]；若first[y - 1] \<\= first[y]，此时first[y]保持不变，但是依然需要使用first[y - 1]来更新second[y]。

到了这里，就得到了first和second，那么对于一组满足x \< y的冲突(x, y)，若first[y] \= x，那么再删去这一组冲突后，以y为右边界的子数组可用的最大左边界就从first[y]变成了second[y]，在之前的基础上新增了first[y] - second[y]个合法的子数组。

不过需要特别注意的是，既然上面first[y]和second[y]的值是通过初始值和first[y - 1]以及second[y - 1]得来的，那么当某个first[y]变为second[y]时，后续可能有部分y'的first值也会跟着产生变化。还是以样例一为例，由于first[4] \= 3是通过first[3] \= 3得到的，那么当first[3] \= 3变为second[3] \= 1时，first[4]也应该从first[4] \= 3变为second[4] \= 2。

也就是说，除了考虑y本身由first变为second之外，还需要考虑每个y可以影响到的后续下标y'，将这些y'的first也变为second。那么在这里还需要从后往前一趟遍历，通过对比相邻位置对应的f\[y\]来确定每个下标y向后最远影响到的下标p\[y\]。具体来说，当first\[y\] \= first\[y + 1\]时，有p\[y\] \= p\[y + 1\]，否则有p\[y\] \= y。这样一来，当某个first\[y\]变为second\[y\]时，从y + 1到p\[y\]之间所有y'对应的first\[y'\]都应该变为second\[y'\]，此时新增的合法子数组的数目为(first\[y\] - second\[y\]) + (first\[y + 1\] - second\[y + 1\]) + ... + (first\[p\[y\]\] - second\[p\[y\]\])。将式子中所有的first项和second项收拢到一起，就变成了first的区间和减去second的区间和的形式，可以通过前缀和之差在O(1)的时间内计算得到。那么在这里还需要额外计算first和second的前缀和sf以及ss，上面式子就可以改写为(sf\[p\[y\]\] - sf\[y - 1\]) - (ss\[p\[y\]\] - ss\[y - 1\])。

最后附上python代码：

```python
class Solution(object):
    def maxSubarrays(self, n, conflictingPairs):
        """
        :type n: int
        :type conflictingPairs: List[List[int]]
        :rtype: int
        """
        
        first = [1] * (n + 1)
        second = [1] * (n + 1)
        for x, y in conflictingPairs:
            if x > y:
                x, y = y, x
            if x + 1 > first[y]:
                first[y], second[y] = x + 1, first[y]
            elif x + 1 > second[y]:
                second[y] = x + 1
        
        sf = [0] * (n + 1)
        ss = [0] * (n + 1)
        now = 0

        for y in range(1, n + 1):
            if first[y - 1] > first[y]:
                second[y] = max(first[y], second[y - 1])
                first[y] = first[y - 1]
            elif first[y - 1] > second[y]:
                second[y] = first[y - 1]
        
            sf[y] = sf[y - 1] + first[y]
            ss[y] = ss[y - 1] + second[y]
            now += y - first[y] + 1
        
        p = [n] * (n + 1)
        for y in range(n - 1, 0, -1):
            if first[y] == first[y + 1]:
                p[y] = p[y + 1]
            else:
                p[y] = y

        res = now
        for x, y in conflictingPairs:
            if x > y:
                x, y = y, x
            
            if x + 1 == first[y]:
                res = max(res, now + (sf[p[y]] - sf[y - 1]) - (ss[p[y]] - ss[y - 1]))
        
        return res
```
