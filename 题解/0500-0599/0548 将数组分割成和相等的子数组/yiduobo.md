---
title: "548. 将数组分割成和相等的子数组"
aliases: ["yiduobo的每日leetcode 548.将数组分割成和相等的子数组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/600969889"
zhihu_id: "600969889"
zhihu_title: "yiduobo的每日leetcode 548.将数组分割成和相等的子数组"
question_id: "548"
question: "将数组分割成和相等的子数组"
problem_url: "https://leetcode.cn/problems/split-array-with-equal-sum/"
difficulty: "Hard"
created: "2023-01-26T00:44:02+08:00"
updated: "2023-01-26T00:44:02+08:00"
upvotes: 0
comments: 0
---

# 548. 将数组分割成和相等的子数组

> **[yiduobo的每日leetcode 548.将数组分割成和相等的子数组](https://zhuanlan.zhihu.com/p/600969889) · 知乎 · 2023-01-26 · 赞同 0**
> 力扣：[548. 将数组分割成和相等的子数组](https://leetcode.cn/problems/split-array-with-equal-sum/) · Hard · 灵茶山艾府：[O(n^2) 前缀和+哈希表](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

548.将数组分割成和相等的子数组

[力扣](https://leetcode.cn/problems/split-array-with-equal-sum/)

题目给出一个数组，要求找出三个分割点i、j、k，将数组分割成四个子数组，且这四个子数组之和相等。

对于子数组的问题，也就是区间和的问题，通常的处理方式是利用前缀和来处理，也就是子数组[left, right]之和可以通过s[right] - s[left - 1]求得，其中s为nums的前缀和数组。

注意到题目的数据规模不大，但是也不算太小，因此O(n^3)的暴力算法是不行的。由于是判断数值是否在之前出现过的问题，那么很自然想到哈希表来进行优化。

具体来说，就是先执行一个二重循环，枚举所有i和j的位置，若当前的s[i - 1] \= s[j - 1] - s[i]，说明如果选择i和j来进行前两次的划分，就可以使得划分出来的前两个子数组之和相等，此时就可以使用一个哈希表left将“以j为结尾的子数组可以完成值为s[i - 1]的二重划分”这一事件记录下来，具体来说就是将s[i - 1]加入到left[j]中，这里的left[j]也是一个集合。

接下来，再执行一个二重循环，这次枚举的是所有j和k的位置。若当前的s[-1] - s[k] \= s[k - 1] - s[j]，说明如果选择j和k来进行后两次的划分，就可以使得划分出来的后两个子数组之和相等，也就是现在有了一个“以j为开头的子数组可以完成值为s[-1] - s[k]的二重划分”。结合上面的“以j为结尾的子数组可以完成值为s[i - 1]的二重划分”，那么如果left[j]中已经存在s[-1] - s[k]，那么就说明找到了一种合法的划分，直接返回true。

若遍历完成都没有找到配对的划分，那么就返回false。

更进一步的，由于i \< j \< k，那么只需要循环按照从小到大的顺序执行，就可以将上面的两次二重循环合并成为一次。另外在枚举这些分割点时，需要注意有严格的边界限制。

最后附上python代码：

```python
class Solution(object):
    def splitArray(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        n = len(nums)

        s = [nums[0]]
        for num in nums[1:]:
            s.append(s[-1] + num)

        left = {}
        for i in range(1, n - 3):
            for j in range(i + 2, n - 1):
                v = s[j - 1] - s[i]
                if s[i - 1] == v:
                    if j not in left:
                        left[j] = set()
                    left[j].add(v)
                
                if v == s[-1] - s[j] and i in left and v in left[i]:
                    return True

        return False
```
