---
title: "269. 火星词典"
aliases: ["yiduobo的每日leetcode 269.火星词典"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/593733794"
zhihu_id: "593733794"
zhihu_title: "yiduobo的每日leetcode 269.火星词典"
question_id: "269"
question: "火星词典"
problem_url: "https://leetcode.cn/problems/alien-dictionary/"
created: "2022-12-23T01:46:12+08:00"
updated: "2022-12-23T01:46:12+08:00"
upvotes: 0
comments: 0
---

# 269. 火星词典

> **[yiduobo的每日leetcode 269.火星词典](https://zhuanlan.zhihu.com/p/593733794) · 知乎 · 2022-12-23 · 赞同 0**
> 力扣：[269. 火星词典](https://leetcode.cn/problems/alien-dictionary/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

269.火星词典

[力扣](https://leetcode.cn/problems/alien-dictionary/)

经典的拓扑排序问题。遍历所有单词，利用单词的前后顺序推导出字符间的大小顺序，并针对这些顺序建立有向图然后执行拓扑排序。

具体来说，就是遍历所有单词，对于当前单词与其上一个单词，再遍历这两个单词中相同下标的所有字符并找出首个不相同的字符。不妨设这两个不相同字符中，属于前一个单词的字符为x，属于后一个单词的字符为y，那么当有向图中没有从x出发到y的边时，就在其中添加一条从x出发到y的边，同时将y的入度加上1。需要注意的是，在这里可能出现找不到不同字符的情况，若这种情况下前一个单词的长度还比当前单词的长度要长，那么就与字典序规则中的第二种情况矛盾了，此时直接返回空字符即可。

构图完成后，先一趟遍历找出所有入度为0的字符，然后进行拓扑排序。拓扑排序完成后，判断拓扑排序队列的长度是否等于出现的字符的数目，若等于，那么拓扑排序的队列就是一种合法的答案，否则说明有向图中存在环，应当返回空字符串。

最后附上python代码：

```python
class Solution(object):
    def alienOrder(self, words):
        """
        :type words: List[str]
        :rtype: str
        """

        ind = {}
        g = {}

        for word in words:
            for char in word:
                if char not in ind:
                    ind[char] = 0
                if char not in g:
                    g[char] = set()

        for i in range(1, len(words)):
            flag = True
            for j in range(min(len(words[i - 1]), len(words[i]))):
                if words[i][j] != words[i - 1][j]:
                    flag = False
                    x, y = words[i - 1][j], words[i][j]
                    if y not in g[x]:
                        g[x].add(y)
                        ind[y] += 1
                    break
            
            if flag and len(words[i - 1]) > len(words[i]):
                return ""
        
        q = []
        for char in ind:
            if ind[char] == 0:
                q.append(char)
        
        head, tail = 0, len(q)
        while head < tail:
            now = q[head]
            head += 1
            for next in g[now]:
                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    tail += 1
        
        if len(q) == len(ind):
            return "".join(q)
        
        return ""
```
