---
title: "2564. 子字符串异或查询"
aliases: ["yiduobo的每日leetcode 2564.子字符串异或查询"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/位运算", "题单/字符串", "题单/位运算/二-异或-XOR-的性质", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/640771861"
zhihu_id: "640771861"
zhihu_title: "yiduobo的每日leetcode 2564.子字符串异或查询"
question_id: "2564"
question: "子字符串异或查询"
problem_url: "https://leetcode.cn/problems/substring-xor-queries/"
difficulty: "Medium"
rating: 1959
created: "2023-07-01T02:18:25+08:00"
updated: "2023-07-01T02:18:25+08:00"
upvotes: 1
comments: 0
---

# 2564. 子字符串异或查询

> **[yiduobo的每日leetcode 2564.子字符串异或查询](https://zhuanlan.zhihu.com/p/640771861) · 知乎 · 2023-07-01 · 赞同 1**
> 力扣：[2564. 子字符串异或查询](https://leetcode.cn/problems/substring-xor-queries/) · Medium · 灵茶山艾府：[预处理 s 中的所有数字（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2564.子字符串异或查询

[力扣](https://leetcode.cn/problems/substring-xor-queries/)

根据异或的性质，有val \= first ^ second，那么本题就是给出若干组询问，对于每组询问(first, second)，找出first ^ second在字符串中首次出现的位置。

由于first和second的取值范围在10^9之内，那么first ^ second的位数不会超过31位，于是可以从1开始到max_l枚举所有二进制子串的长度，这里的max_l为所有询问中first ^ second的结果在二进制下的最大位数。

对于当前枚举到的子串长度l，则可以使用一个长度为l的滑动窗口从左向右滑动，找出字符串中所有长度为l的子串，并使用一个哈希表记录这些子串对应的十进制值首次出现的下标。

求解完成后，就可以利用这个哈希表在O(1)的时间内完成单词查询的求解。

最后附上python代码：

```python
class Solution(object):
    def substringXorQueries(self, s, queries):
        """
        :type s: str
        :type queries: List[List[int]]
        :rtype: List[List[int]]
        """

        num_list = []
        max_l = 0
        for first, second in queries:
            num_list.append(first ^ second)
            max_l = max(max_l, len(bin(num_list[-1])) - 2)
        
        pos = {}
        for l in range(1, max_l + 1):
            if l > len(s):
                break
            
            now = 0
            for char in s[:l]:
                now += now
                if char == '1':
                    now += 1
            
            if now not in pos:
                pos[now] = 0

            for index, char in enumerate(s[l:]):
                if s[index] == '1':
                    now -= (1 << (l - 1))
                
                now += now
                if char == '1':
                    now += 1
                
                if now not in pos:
                    pos[now] = index + 1
        
        res = []
        for num in num_list:
            if num not in pos:
                res.append([-1, -1])
            else:
                res.append([pos[num], pos[num] + len(bin(num)) - 3])
        
        return res
```
