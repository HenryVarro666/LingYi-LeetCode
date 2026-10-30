---
title: "3734. 大于目标字符串的最小字典序回文排列"
aliases: ["yiduobo的每日leetcode 3734.大于目标字符串的最小字典序回文排列"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1968766034619105684"
zhihu_id: "1968766034619105684"
zhihu_title: "yiduobo的每日leetcode 3734.大于目标字符串的最小字典序回文排列"
question_id: "3734"
question: "大于目标字符串的最小字典序回文排列"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-palindromic-permutation-greater-than-target/"
difficulty: "Hard"
rating: 2330
created: "2025-11-04T21:20:36+08:00"
updated: "2025-11-04T21:20:40+08:00"
upvotes: 1
comments: 0
---

# 3734. 大于目标字符串的最小字典序回文排列

> **[yiduobo的每日leetcode 3734.大于目标字符串的最小字典序回文排列](https://zhuanlan.zhihu.com/p/1968766034619105684) · 知乎 · 2025-11-04 · 赞同 1**
> 力扣：[3734. 大于目标字符串的最小字典序回文排列](https://leetcode.cn/problems/lexicographically-smallest-palindromic-permutation-greater-than-target/) · Hard · 灵茶山艾府：[O(n) 倒序贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3734.大于目标字符串的最小字典序回文排列

[3734. 大于目标字符串的最小字典序回文排列 - 力扣（LeetCode）](https://leetcode.cn/problems/lexicographically-smallest-palindromic-permutation-greater-than-target/description/)

题目给出两个长度都为n的字符串s以及目标字符串target，这两个字符串都有小写英文字母组成。

要求将s中的字符重新排列，得到一个回文这个字符串，这个字符串的字典序要严格大于target。问可能得到的字典序最小的字符串是什么。若不存在，则返回空字符串。

由于最终需要构成回文串，那么可以先进行一趟遍历，记录每种字符出现的次数。

若出现次数为奇数的字符超过1个，那么就必然无法构成回文串，此时应该返回空字符串。

若出现次数为奇数的字符恰好只有1个，那么这个字符必然要放在最终答案的正中间，记录这个字符为mid。

若没有出现次数为奇数的字符，则可以记录mid为空。

接下来，将所有字符的出现次数除以2，就得到了构成回文串左半部分的每种字符出现的次数。现在需要使用这些字符构成一个字典序最小的字符串，这个字符串需要满足一下两个条件之一：

1、这个字符串的字典序大于target的前半部分

2、这个字符串的字典序与target的前半部分相同，同时中间字符mid，再加上这个字符串反转后得到的字符串，其字典序大于target的后半部分

无论是哪种情况，都期望得到一个字典序最小，且大于等于target的前半部分的字符串，那么就可以从最左侧开始，顶着target的前半部分逐个字符填充答案字符串，直到填充完整个字符串，或者没有与target当前位置相同的字符位置。

若填充完了整个字符串，那么就说明目前填充的字符串与target的前半部分完全相同，此时需要检测mid拼接上当前字符串反转后的字符串，是否大于target的后半部分。若大于，那么就得到了最终答案，若小于或等于，则需要进行调整。

此时可以从最后一个字符开始向前遍历，对于当前位置，先弹出当前位置上已经填充的字符，然后查找剩余字符中是否存在某个字符，其字典序大于target在当前位置上的字符。若存在，则将其填充到当前位置上，然后再将剩余的字符按字典序从小到大填充到剩余的位置上即可；若不存在，则继续向前遍历，尝试修改前一个字符。重复此过程，直到修改成功或者全部字符都被弹出为止。若修改成功，那么修改后得到的字符串，加上mid，再加上该字符串反转后的结果即为最终答案；若没有修改成功，则返回空字符串。

若没能填充完整个字符串，那么就需要提早从当前无法填充的位置开始进行调整，调整的方式与上面相同。

最后附上python代码：

```python
class Solution(object):
    def lexPalindromicPermutation(self, s, target):
        """
        :type s: str
        :type target: str
        :rtype: str
        """
        
        cnt = {}
        for c in s:
            cnt[c] = cnt.get(c, 0) + 1
        
        mid = ""
        for c in cnt:
            if cnt[c] % 2 == 1:
                if mid != "":
                    return ""
                mid = c
            cnt[c] //= 2
        
        half = []
        p = len(target) // 2 - 1
        for i in range(len(target) // 2):
            if cnt.get(target[i], 0) > 0:
                half.append(target[i])
                cnt[target[i]] -= 1
            else:
                p = i
                break

        if len(half) == len(target) // 2:
            s = ''.join(half) + mid + ''.join(half[::-1])
            if s > target:
                return s
            
            if half:
                cnt[half.pop()] += 1

        while p >= 0:
            for i in range(ord(target[p]) + 1, 123):
                c = chr(i)
                if cnt.get(c, 0) > 0:
                    half.append(c)
                    cnt[c] -= 1
                
                    for j in range(26):
                        c = chr(j + 97)
                        while cnt.get(c, 0) > 0:
                            half.append(c)
                            cnt[c] -= 1
                    
                    return ''.join(half) + mid + ''.join(half[::-1])
            
            if half:
                cnt[half.pop()] += 1
            p -= 1
        
        return ""
```
