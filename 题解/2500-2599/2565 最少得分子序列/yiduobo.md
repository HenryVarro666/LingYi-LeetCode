---
title: "2565. 最少得分子序列"
aliases: ["yiduobo的每日leetcode 2565.最少得分子序列"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/two-pointers", "leetcode/string", "题单/滑动窗口与双指针", "题单/动态规划", "题单/滑动窗口与双指针/四-双序列双指针", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/640913999"
zhihu_id: "640913999"
zhihu_title: "yiduobo的每日leetcode 2565.最少得分子序列"
question_id: "2565"
question: "最少得分子序列"
problem_url: "https://leetcode.cn/problems/subsequence-with-the-minimum-score/"
difficulty: "Hard"
rating: 2432
created: "2023-07-02T00:49:57+08:00"
updated: "2023-07-02T00:49:57+08:00"
upvotes: 0
comments: 0
---

# 2565. 最少得分子序列

> **[yiduobo的每日leetcode 2565.最少得分子序列](https://zhuanlan.zhihu.com/p/640913999) · 知乎 · 2023-07-02 · 赞同 0**
> 力扣：[2565. 最少得分子序列](https://leetcode.cn/problems/subsequence-with-the-minimum-score/) · Hard · 灵茶山艾府：[前后缀分解+判断子序列（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2565.最少得分子序列

[力扣](https://leetcode.cn/problems/subsequence-with-the-minimum-score/)

题目要求从t中删除一个子序列，使得新的t成为s的一个子序列，且删除子序列的左右边界之间距离最短。

注意到题目要求的是左右边界之间距离最短，那么在这里就可以将左右边界之间的字符全部删除方便计算。可以这样处理的原因是对于a的某个子序列b，从b中删去若干字符得到的子序列c依然是a的子序列。那么对于本题，如果从t中删去左右边界分别为left和right的某个子序列后得到的新的t是s的子序列，那么将新t中所有从原始t的left到right之间的字符也删去，得到的子序列依然是s的子序列，且左右边界之间的距离不变。

到了这里，问题就变成了从t中删去一个最短的子串，使得新的t为s的一个子序列。

很明显，删除的子串长度越长，新的t是s子序列的可能性就越大，因此在这里可以通过二分答案来确定最终删去的子串的长度。

对于当前二分到的子串长度mid，则可以从左到右一趟遍历，枚举t中所有长度为t的子串的起点p，那么此时的t就被切分成了前缀t[:p]以及后缀t[p + mid:]。到了这里，问题就变成了能否将s也分为两个部分s[:pre]和s[suf:]，其中t[:p]是s[pre]的子序列，t[p + mid:]是s[suf]的子序列，同时pre \< suf。

对于这个问题，可以使用贪心法一趟遍历求解，但这样一来时间复杂度就太高了。另一种处理方法是先进行预处理，使用一个数组prefix记录适配t的所有前缀所需的s的最短前缀的终点。

更具体的，对于prefix[i]，记录的是使得t[:i + 1]是s[:prefix[i] + 1]的子序列的最小值。那么对于prefix，只需一趟遍历即可求解。同样的，使用另一个数组suffix记录适配t的所有后缀所需的s的最短后缀的起点。这样一来，就可以在O(1)的时间内找出每一组t[:p]和t[p + mid:]对应的pre和suf了。

最后附上python代码：

```python
class Solution(object):
    def minimumScore(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: int
        """

        prefix = []
        p = 0
        for char in t:
            while p < len(s) and s[p] != char:
                p += 1
            prefix.append(p)
            if p < len(s):
                p += 1
        
        suffix = []
        p = len(s) - 1
        for char in t[::-1]:
            while p >= 0 and s[p] != char:
                p -= 1
            suffix.append(p)
            if p >= 0:
                p -= 1
        
        suffix.reverse()
        
        if prefix[-1] < len(s):
            return 0
        

        left = 1
        right = len(t)
        while left < right:
            mid = (left + right) >> 1
            flag = False
            for pre_len in range(len(t) - mid + 1):
                suf_len = len(t) - mid - pre_len
                if pre_len == 0:
                    pre_pos = -1
                else:
                    pre_pos = prefix[pre_len - 1]

                if suf_len == 0:
                    suf_pos = len(s)
                else:
                    suf_pos = suffix[len(t) - suf_len]

                if pre_pos < suf_pos:
                    flag = True
                    break
            
            if flag:
                right = mid
            else:
                left = mid + 1
        
        return left
```
