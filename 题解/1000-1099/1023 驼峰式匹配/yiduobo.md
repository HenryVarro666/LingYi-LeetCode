---
title: "1023. 驼峰式匹配"
aliases: ["yiduobo的每日leetcode 1023.驼峰式匹配"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/368939895"
zhihu_id: "368939895"
zhihu_title: "yiduobo的每日leetcode 1023.驼峰式匹配"
question_id: "1023"
question: "驼峰式匹配"
problem_url: "https://leetcode.cn/problems/camelcase-matching/"
created: "2021-04-29T23:41:51+08:00"
updated: "2021-04-29T23:41:51+08:00"
upvotes: 0
comments: 0
---

# 1023. 驼峰式匹配

> **[yiduobo的每日leetcode 1023.驼峰式匹配](https://zhuanlan.zhihu.com/p/368939895) · 知乎 · 2021-04-29 · 赞同 0**
> 力扣：[1023. 驼峰式匹配](https://leetcode.cn/problems/camelcase-matching/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1023.驼峰式匹配

[力扣](https://leetcode-cn.com/problems/camelcase-matching/)

首先可以明确的一点是，若queries中字符串的大写字母数量与pattern中大写字母的数量不一致，那么这条query必然是无法匹配的，可以直接忽略掉。

对于剩下的query，则可以通过构造trie树来为之后的匹配做准备。由于题目要求是哪些query可以匹配上，那么在构造trie树时除了必备的字母dict之外，还需要一个list来额外储存能够匹配当前前缀的query有哪些。

构造好trie树后，需要注意这里不能直接一个个字符匹配，而需要执行dfs，因为trie树中的小写字母是可以被跳过的。那么我们从trie树的根节点以及待匹配的字符下标0开始进行dfs，对于当前的子树now以及待匹配的字符下标pos：

1、若此时pos等于len(pattern)，说明此时pattern已经完成了匹配，说明pattern可以匹配上所有当前节点储存的list中的所有query，于是将这些query的结果置为true然后返回。

2、若此时pattern\[pos\]出现在now的字母字典中，那么说明pattern\[now\]形成了匹配，那么此时就应该从子树now\[pattern\[pos\]\]以及待匹配的字符下标pos + 1继续进行dfs。

3、另外对于now的字母字典中的所有小写字符lower_char，跳过也是一个可行的选项，那么此时已然需要匹配字符下标pos的字母，但是子树变成了now[lower_char]，于是此时应该从now[lower_pos]以及pos继续进行dfs。

最后附上python代码：

```python
class Solution(object):
    def camelMatch(self, queries, pattern):
        """
        :type queries: List[str]
        :type pattern: str
        :rtype: List[bool]
        """

        up_cnt = 0
        for char in pattern:
            if 'A' <= char <= 'Z':
                up_cnt += 1

        trie = [{}, []]
        for index, query in enumerate(queries):
            tmp = 0
            for char in query:
                if 'A' <= char <='Z':
                    tmp += 1
            if tmp != up_cnt:
                continue

            now = trie
            for char in query:
                if char not in now[0]:
                    now[0][char] = [{}, [index]]
                else:
                    now[0][char][1].append(index)
                now = now[0][char]

        res = [False] * len(queries)

        self.dfs(trie, pattern, 0, res)
        return res
    
    def dfs(self, now, pattern, pos, res):
        if pos == len(pattern):
            for index in now[1]:
                res[index] = True
            return
        
        for next_char in now[0]:
            if next_char == pattern[pos]:
                self.dfs(now[0][next_char], pattern, pos + 1, res)
            elif 'a' <= next_char <= 'z':
                self.dfs(now[0][next_char], pattern, pos, res)
```
