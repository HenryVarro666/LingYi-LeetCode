---
title: "2157. 字符串分组"
aliases: ["yiduobo的每日leetcode 2157.字符串分组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/union-find", "leetcode/hash-table", "leetcode/string", "题单/常用数据结构", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/531525258"
zhihu_id: "531525258"
zhihu_title: "yiduobo的每日leetcode 2157.字符串分组"
question_id: "2157"
question: "字符串分组"
problem_url: "https://leetcode.cn/problems/groups-of-strings/"
difficulty: "Hard"
rating: 2499
created: "2022-06-21T00:11:30+08:00"
updated: "2022-06-21T00:11:30+08:00"
upvotes: 0
comments: 0
---

# 2157. 字符串分组

> **[yiduobo的每日leetcode 2157.字符串分组](https://zhuanlan.zhihu.com/p/531525258) · 知乎 · 2022-06-21 · 赞同 0**
> 力扣：[2157. 字符串分组](https://leetcode.cn/problems/groups-of-strings/) · Hard · 灵茶山艾府：[哈希并查集 + 位运算（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2157.字符串分组

[力扣](https://leetcode.cn/problems/groups-of-strings/)

如果将每种字符串视为无向图中的一个点，两个字符串直接的关联视为无向图中的一条边的话，题目实际上就是要找出这张图中有多少个连通分量，以及最大的连通分量中有多少个节点。这个问题可以通过bfs求解得到，具体来说就是遍历每个节点，若当前节点没有被之前进行的bfs访问过，那么就从当前节点开始进行bfs，将连通分量的总数加上1，并使用当前bfs队列的长度来更新答案。

接下来的问题是如何建图。题目中字符串的数目最多可达两万个，那么两两枚举字符串判断是否关联显然是行不通的。注意到题目中的字符串只包含小写字符，且每个字符只出现一次，那么对于题目中的添加、删除、替换这三种操作，在不进行任何剪枝的情况下最多也只有26 + 26 + 26^2种可能的情况。换言之，与图中某个节点相连的边最多也只有这么多，因此可以转换思路，在bfs时不枚举而是枚举边，然后通过点和边来计算边另一端的点，通过判断该点是否在最初的words中从而判断当前枚举的边是否存在于图中。

当然，直接进行字符串操作判断复杂度还是很高，在这里很自然想到使用2^26的状态压缩编码来表示每种字符串。这样一来，就可以通过位运算在均摊O(1)的时间内求出添加、删除、替换后的每种字符串编码。而对于判断是否在最初的words中，则可以使用哈希表先记录words中所有字符串的编码，然后通过哈希表来进行判断。

最后附上python代码：

```python
class Solution(object):
    def groupStrings(self, words):
        """
        :type words: List[str]
        :rtype: List[int]
        """

        num_list = []
        num_dict = {}
        for word in words:
            now = 0
            for char in word:
                now |= (1 << ord(char) - 97)
            num_list.append(now)
            num_dict[now] = num_dict.get(now, 0) + 1
        
        used = set()
        cnt = 0
        max_len = 0
        for num in num_list:
            if num not in used:
                cnt += 1
                q = [num]
                l = 0
                r = 1
                now_len = num_dict[num]
                used.add(num)
                while l < r:
                    now = q[l]
                    l += 1
                    for index in range(26):
                        next = now | (1 << index)
                        if next in num_dict and next not in used:
                            q.append(next)
                            used.add(next)
                            r += 1
                            now_len += num_dict[next]
                        
                        if (now & (1 << index)):
                            next = now ^ (1 << index)
                            if next in num_dict and next not in used:
                                q.append(next)
                                used.add(next)
                                r += 1
                                now_len += num_dict[next]
                            
                            tmp = next
                            for rep in range(26):
                                next = tmp | (1 << rep)
                                if next in num_dict and next not in used:
                                    q.append(next)
                                    used.add(next)
                                    r += 1
                                    now_len += num_dict[next]
                
                max_len = max(max_len, now_len)
        
        return [cnt, max_len]
```
