---
title: "3167. 字符串的更好压缩"
aliases: ["yiduobo的每日leetcode 3167.字符串的更好压缩"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/704900016"
zhihu_id: "704900016"
zhihu_title: "yiduobo的每日leetcode 3167.字符串的更好压缩"
question_id: "3167"
question: "字符串的更好压缩"
problem_url: "https://leetcode.cn/problems/better-compression-of-string/"
created: "2024-06-23T01:13:03+08:00"
updated: "2024-06-23T01:13:03+08:00"
upvotes: 0
comments: 0
---

# 3167. 字符串的更好压缩

> **[yiduobo的每日leetcode 3167.字符串的更好压缩](https://zhuanlan.zhihu.com/p/704900016) · 知乎 · 2024-06-23 · 赞同 0**
> 力扣：[3167. 字符串的更好压缩](https://leetcode.cn/problems/better-compression-of-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3167.字符串的更好压缩

[. - 力扣（LeetCode）](https://leetcode.cn/problems/better-compression-of-string/description/)

题目给出一个压缩字符串compressed，其格式为一个字符c加上一个频率x，表示这个字符c出现了x次。例如'a3b1a1c2'是'aaabacc'的压缩。现在要求将其重新压缩，使得最终的字符串中每种字符只出现一次，且按字典序排好。

题目实际上就是要统计原字符串中每种字符串出现的次数，由于compressed的格式固定，那么就可以利用双指针一趟遍历，将每一组(字符，频率)都分离出来，然后使用哈希表将每种字符的频率累加起来，得到原字符串中每种字符出现的次数。

对于分离子段这个问题，不妨设当前子串的起点为p，那么compressed[p]一定就是那个字符，接下来令q从p + 1开始不断向后遍历，直到q来到compressed的末尾或者compressed[q]不是数字为止，那么compressed[p + 1: q]就是那个频率。将其累加到哈希表中并将p更新为q，重复上面的过程直到p来到compressed的末尾为止。

得到哈希表后，将其中的字符按字典序遍历，与其出现次数拼接构造答案字符串即可。

最后附上python代码：

```python
class Solution(object):
    def betterCompression(self, compressed):
        """
        :type compressed: str
        :rtype: str
        """

        freq = Counter()
        p = 0
        while p < len(compressed):
            char = compressed[p]
            q = p + 1
            while q < len(compressed) and '0' <= compressed[q] <= '9':
                q += 1
            
            freq[char] += int(compressed[p + 1 : q])
            p = q
        
        return ''.join([char + str(freq[char]) for char in sorted(freq.keys())])
```
