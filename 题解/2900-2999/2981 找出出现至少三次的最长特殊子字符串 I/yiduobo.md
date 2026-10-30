---
title: "2981. 找出出现至少三次的最长特殊子字符串I & 2982. 找出出现至少三次的最长特殊子字符串II"
aliases: ["yiduobo的每日leetcode 2981.找出出现至少三次的最长特殊子字符串I && 2982.找出出现至少三次的最长特殊子字符串II", "2981. 找出出现至少三次的最长特殊子字符串I", "2982. 找出出现至少三次的最长特殊子字符串II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "题单/二分算法", "题单/贪心算法", "题单/二分算法/二-二分答案", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/692357038"
zhihu_id: "692357038"
zhihu_title: "yiduobo的每日leetcode 2981.找出出现至少三次的最长特殊子字符串I && 2982.找出出现至少三次的最长特殊子字符串II"
question_id: ["2981", "2982"]
question: ["找出出现至少三次的最长特殊子字符串 I", "找出出现至少三次的最长特殊子字符串 II"]
problem_url: ["https://leetcode.cn/problems/find-longest-special-substring-that-occurs-thrice-i/", "https://leetcode.cn/problems/find-longest-special-substring-that-occurs-thrice-ii/"]
difficulty: "Medium"
rating: 1773
created: "2024-04-14T02:10:26+08:00"
updated: "2024-04-14T02:10:26+08:00"
upvotes: 1
comments: 0
---

# 2981. 找出出现至少三次的最长特殊子字符串I & 2982. 找出出现至少三次的最长特殊子字符串II

> **[yiduobo的每日leetcode 2981.找出出现至少三次的最长特殊子字符串I && 2982.找出出现至少三次的最长特殊子字符串II](https://zhuanlan.zhihu.com/p/692357038) · 知乎 · 2024-04-14 · 赞同 1**
> 力扣：[2981. 找出出现至少三次的最长特殊子字符串 I](https://leetcode.cn/problems/find-longest-special-substring-that-occurs-thrice-i/) · Medium · 灵茶山艾府：[非暴力做法，分类讨论（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)
> 力扣：[2982. 找出出现至少三次的最长特殊子字符串 II](https://leetcode.cn/problems/find-longest-special-substring-that-occurs-thrice-ii/) · Medium · 灵茶山艾府：[分类讨论，简洁写法（Python/Java/C++/Go/JS/Rust）](../2982%20找出出现至少三次的最长特殊子字符串%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2981.找出出现至少三次的最长特殊子字符串I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-longest-special-substring-that-occurs-thrice-i/)

2982.找出出现至少三次的最长特殊子字符串II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-longest-special-substring-that-occurs-thrice-ii/description/)

两题的题面是一样的，后面这题的数据规模扩大了很多，需要找出一个O(n)的算法。

观察题目给出的样例一可以发现，对于一个长度为k的由相同字符构成的子串，可以拆除三个长度为k - 2的子串，也就是s[:k - 2]，s[1 : k - 1]，s[2 : k]这三个长度为k - 2的子串。更进一步的，其也可以提供两个长度为k - 1的子串以及一个长度为k的子串。

那么在这里可以先一趟遍历，将所有由相同字符的子串提取出来，然后按字符将这些子串的长度都收集起来。接下里对于每个字符，考察其所有出现的长度：

1、可以通过上面讨论的方法，将最长的那个拆成三个，于是可以用最长的长度减2来更新答案。

2、若存在至少两个字符串，那么可以取出其中长度的前两名。若二者长度相同，那么就只能提取出一共4个长度为最长长度减1的子串，于是可以用最长的长度减1来更新答案；若长度不相同，那么最长的子串中至少包含了两个次长的子串，因此可以用次长的长度来更新答案。

3、若存在至少三个字符串，那么一定可以用排名第三的长度来更新答案。

最后附上python代码：

```python
class Solution(object):
    def maximumLength(self, s):
        """
        :type s: str
        :rtype: int
        """

        length_dict = {}
        p = 0
        while p < len(s):
            q = p
            while q + 1 < len(s) and s[q + 1] == s[q]:
                q += 1
            
            if s[p] not in length_dict:
                length_dict[s[p]] = []
            length_dict[s[p]].append(q - p + 1)
            p = q + 1
        
        res = 0
        for char in length_dict:
            length_list = sorted(length_dict[char], reverse=True)
            res = max(res, length_list[0] - 2)
            if len(length_list) > 1:
                if length_list[1] == length_list[0]:
                    res = max(res, length_list[0] - 1)
                else:
                    res = max(res, length_list[1])
            if len(length_list) > 2:
                res = max(res, length_list[2])
        
        if res == 0:
            res = -1
        return res
```
