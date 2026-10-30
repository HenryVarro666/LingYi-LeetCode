---
title: "2193. 得到回文串的最少操作次数"
aliases: ["yiduobo的每日leetcode 2193.得到回文串的最少操作次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/537593435"
zhihu_id: "537593435"
zhihu_title: "yiduobo的每日leetcode 2193.得到回文串的最少操作次数"
question_id: "2193"
question: "得到回文串的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-moves-to-make-palindrome/"
created: "2022-07-05T00:47:43+08:00"
updated: "2022-07-05T00:47:43+08:00"
upvotes: 0
comments: 0
---

# 2193. 得到回文串的最少操作次数

> **[yiduobo的每日leetcode 2193.得到回文串的最少操作次数](https://zhuanlan.zhihu.com/p/537593435) · 知乎 · 2022-07-05 · 赞同 0**
> 力扣：[2193. 得到回文串的最少操作次数](https://leetcode.cn/problems/minimum-number-of-moves-to-make-palindrome/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2193.得到回文串的最少操作次数

[力扣](https://leetcode.cn/problems/minimum-number-of-moves-to-make-palindrome/)

贪心法的题目，但是没有想到比较严谨的证明可以证明我的做法是全局最优。

首先，两个相同的字符之间是不应该发生交换的，相当于浪费了一次操作。从这个节点可以引申出每个字符对应的匹配字符从一开始就固定好了，可以按从两侧向中心的方式寻找到每个字符的匹配字符。

接下来，对于一组匹配字符而言，确定其最终所处的位置就能计算出需要移动的步骤数。由于考虑左右是等价的，因此在这里不妨设二者的位置分别为i和n - 1 - j，其中i \<\= j，也就是左侧的字符更靠近边界。可以发现，只有当左侧的字符最终位置在i到n - j - 1之间时，两个字符的总移动次数才会最少，在这里简单说明一下：

1、当左侧字符的最终位置p在0到i - 1之间时，其对称位置n - 1 - p必然不在j的左侧，因此二者的总移动次数为

cnt1 \= i - p + n - 1 - p - j \= n - 1 + i - j - p - p

2、当左侧字符的最终位置p在i到n - 1 - j之间时，其对称位置n - 1 - p同样不在j的左侧，因此二者的总移动次数为

cnt2 \= p - i + n - 1 - p - j \= n - 1 - i - j

3、当左侧字符的最终位置p大于n - 1 - j时，其对称位置n - 1 - p在p的左侧，因此二者的总移动次数为

cnt3 \= p - i + j - (n - 1 - p) \= -(n - 1) - i + j + p + p

首先对比cnt1和cnt2。由于cnt2中没有出现p，在这里的p都是指的cnt1中满足0 \<\= p \< i的p。

cnt1 - cnt2 \= i + i - p - p > 0，即cnt1 > cnt2

接下来对比cnt2和cnt3。同样的，这里的p指的是cnt3中满足n - 1 - j \< p的p。

cnt2 - cnt3 \= 2 \* (n - 1 - p) - 2 \* j \= 2 \* (n - 1 - p - j) \< 0，即cnt2 \< cnt3

综合起来，就是只有当左侧字符的最终位置p在i到n - j - 1之间时操作的次数才最少。

更一般的，就是对于一组匹配的字符s[i]和s[j]，设s[i]是更靠近边界的那一个，那么只有当s[i]最终位于i到n - j - 1之间时操作的次数才最少。

根据上面的结论，就可以从左向右一趟遍历，对于当前的左侧字符，找到最右侧的相同字符，然后将右侧的字符移动到当前左侧位置对称的地方。

上面这个做法可以保证使得每一组字符匹配的操作次数都是最少的，同时从两侧往中间移动避免了后面字符的操作影响到已经就位的字符，勉强达到了全局最优，但是并没有想出更严谨更数学的证明。

另外需要注意的是，对于奇数长度的字符串存在一个落单的中间字符，其需要操作数就是该字符距离n / 2的距离，但是在其他字符就位前不应该移动这个字符，例如caabbbb这种情况，第二个a应该一直向右侧交换，但是如果先移动c，就相当于第二个a进行了一次不必要的左侧交换。

上面朴素的做法时间复杂度为O(n^2)，对于本题是完全足够了。当数据规模更大时，可以考虑类似排队问题的做法，先找出每个字符的目标位置，然后利用树状数组计算每个字符与目标位置之间现存的字符总数，从而省去交换的步骤高效地计算出答案。

最后附上python代码：

```python
class Solution(object):
    def minMovesToMakePalindrome(self, s):
        """
        :type s: str
        :rtype: int
        """

        n = len(s)
        s_list = list(s)
        l = 0
        r = n - 1
        res = 0
        while l < r:
            p = r
            while p > l and s_list[p] != s_list[l]:
                p -= 1
            if p == l:
                res += n / 2 - l
                l += 1
            else:
                for index in range(p, r):
                    s_list[index], s_list[index + 1] = s_list[index + 1], s_list[index]
                    res += 1
                l += 1
                r -= 1
        
        return res
```
