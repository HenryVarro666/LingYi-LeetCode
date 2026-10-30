---
title: "2584. 分割数组使乘积互质"
aliases: ["yiduobo的每日leetcode 2584.分割数组使乘积互质"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/贪心算法", "题单/数学算法/一-数论", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/642745854"
zhihu_id: "642745854"
zhihu_title: "yiduobo的每日leetcode 2584.分割数组使乘积互质"
question_id: "2584"
question: "分割数组使乘积互质"
problem_url: "https://leetcode.cn/problems/split-the-array-to-make-coprime-products/"
difficulty: "Hard"
rating: 2159
created: "2023-07-11T04:34:12+08:00"
updated: "2023-07-11T04:34:12+08:00"
upvotes: 0
comments: 0
---

# 2584. 分割数组使乘积互质

> **[yiduobo的每日leetcode 2584.分割数组使乘积互质](https://zhuanlan.zhihu.com/p/642745854) · 知乎 · 2023-07-11 · 赞同 0**
> 力扣：[2584. 分割数组使乘积互质](https://leetcode.cn/problems/split-the-array-to-make-coprime-products/) · Hard · 灵茶山艾府：[本质是跳跃游戏（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2584.分割数组使乘积互质

[力扣](https://leetcode.cn/problems/split-the-array-to-make-coprime-products/)

题目给出一个数组，要求找出一个最短的前缀，使得前缀中所有数的乘积与剩余的数的乘积互质。

对于与互质有关的问题，常见的做法是先分解质因数，然后转化为质因数出现次数的问题。对于本题，可以认为是要求找出一个最短的前缀，要求前缀中所有数的质因子都不是剩余的数的约数，也就是说这些质因数最后出现的位置都不超过前缀的右边界。

为了方便后续的计算，可以先通过筛法找出数据范围内所有数的最大的质因数，这样一来对于数组中的每个数，就可以高效地完成分解质因数的操作。为了得到每个质因数最后出现的位置，就可以逆序遍历数组，使用一个集合数组prime_set_list储存每个位置的所有质因数，同时使用一个哈希表last记录每种质因数最后出现的位置。对于当前遍历到的数nums[index]，将其分解质因数，并将这些质因数加入到prime_set_list[index]中，同时使用当前下标index更新last中这些质因数最后一次出现的位置。

接下来，从位置0到n - 2遍历数组，计算当前前缀中所有数分解质因数后，所有质因数最后一次出现位置的最大值。对于前缀nums[:index + 1]对应的最大值的求解，只需在nums[:index]对应的最大值的基础上，利用当前右边界上的数nums[index]的所有质因数，也就是prime_set_list[index]中记录的所有质因数最后出现的位置来更新nums[:index + 1]对应的最大值就行了。若当前的最大值等于当前遍历到的位置，说明index即为最终答案，直接返回index即可，否则的话就需要继续向后遍历。若遍历完成任然没有找到答案，则返回-1。

最后附上python代码：

```python
class Solution(object):
    def findValidSplit(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        f = [None] * 1000001
        x = 2
        while x <= 1000:
            if f[x] is None:
                f[x] = x
                for y in range(x + x, 1000001, x):
                    f[y] = x
            x += 1
        
        n = len(nums)
        prime_set_list = [set() for _ in range(n)]
        last = {}
        for index in range(n - 1, -1, -1):
            now = nums[index]
            while f[now] is not None:
                prime_set_list[index].add(f[now])
                if f[now] not in last:
                    last[f[now]] = index
                now /= f[now]
            if now != 1:
                prime_set_list[index].add(now)
                if now not in last:
                    last[now] = index
        
        res = 0
        for index in range(n - 1):
            for p in prime_set_list[index]:
                res = max(res, last[p])
            
            if res == index:
                return res
        
        return -1
```
