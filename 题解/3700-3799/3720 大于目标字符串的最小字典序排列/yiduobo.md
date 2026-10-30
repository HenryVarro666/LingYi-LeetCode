---
title: "3720. 大于目标字符串的最小字典序排列"
aliases: ["yiduobo的每日leetcode 3720.大于目标字符串的最小字典序排列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/78290430764"
zhihu_id: "78290430764"
zhihu_title: "yiduobo的每日leetcode 3720.大于目标字符串的最小字典序排列"
question_id: "3720"
question: "大于目标字符串的最小字典序排列"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-permutation-greater-than-target/"
difficulty: "Medium"
rating: 1958
created: "2025-10-20T21:51:07+08:00"
updated: "2025-10-20T21:51:11+08:00"
upvotes: 4
comments: 0
---

# 3720. 大于目标字符串的最小字典序排列

> **[yiduobo的每日leetcode 3720.大于目标字符串的最小字典序排列](https://zhuanlan.zhihu.com/p/78290430764) · 知乎 · 2025-10-20 · 赞同 4**
> 力扣：[3720. 大于目标字符串的最小字典序排列](https://leetcode.cn/problems/lexicographically-smallest-permutation-greater-than-target/) · Medium · 灵茶山艾府：[O(n) 倒序贪心，附相似题目（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3720.大于目标字符串的最小字典序排列

[3720. 大于目标字符串的最小字典序排列 - 力扣（LeetCode）](https://leetcode.cn/problems/lexicographically-smallest-permutation-greater-than-target/)

题目给出两个长度为n且仅由小写字符组成的字符串s以及target。

要求将s中的字符重新排列，使得其字典序严格大于target，同时字典序最小。若不存在合法的排列，则返回空字符串。

首先处理无解的情况。使用一个哈希表cnt将s中所有字符都收集起来，接下来按从'z'到'a'的顺序遍历，将cnt中对应数量的字符添加到字符串t中，这样一来就得到了s可能构成的字典序最大的排列。若t还是小于等于target，那么就说明没有合法的排列，可以直接返回空字符串。

反之，则需要想办法构造一个刚好比target大一丁点，但是字典序又最小的排列。

最理想的情况就是得到的字符串的前缀都与target一样，仅有最后一个字符比target的最后一个字符更大。当然，这种情况是可遇不可求的，但是可以沿着这个思路进行构造：尽量按照target来填充答案字符串的前缀，直到不存在对应的字符，或者填充完除最后一个字符外的其他字符为止。接下来，填充一个比target当前字符稍微大一点的字符，然后对于剩下的字符，按照从小到大的顺序进行填充就行。

当然，也可能出现不存在稍微大一点的字符的情况，那么就必须回溯，尝试在当前位置的前一位填充稍微大一点的字符，然后将剩下字符按从小到大的顺序进行填充。若前一位也不存在稍微大一点的字符，则继续往前回溯，直到找到一个有字符可填的位置为止。由于一开始排除掉了无解的情况，因此必然可以找到这么一个位置。

最后附上python代码：

```python
class Solution(object):
    def lexGreaterPermutation(self, s, target):
        """
        :type s: str
        :type target: str
        :rtype: str
        """
        
        cnt = {}
        for c in s:
            cnt[c] = cnt.get(c, 0) + 1
        
        t = ""
        for index in range(25, -1, -1):
            c = chr(index + 97)
            t += c * cnt.get(c, 0)

        if t <= target:
            return ''
        
        res = []
        p = 0
        while p < len(target) - 1 and cnt.get(target[p], 0) > 0:
            cnt[target[p]] -= 1
            res.append(target[p])
            p += 1

        while True:
            c = chr(ord(target[p]) + 1)
            while c <= 'z' and cnt.get(c, 0) == 0:
                c = chr(ord(c) + 1)
            
            if c <= 'z':
                res.append(c)
                cnt[c] -= 1
                for index in range(26):
                    c = chr(index + 97)
                    res.append(c * cnt.get(c, 0))
                return ''.join(res)
            
            p -= 1
            res.pop()
            cnt[target[p]] += 1
```
