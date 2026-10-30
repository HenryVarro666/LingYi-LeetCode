---
title: "1772. 按受欢迎程度排列功能"
aliases: ["yiduobo的每日leetcode 1772.按受欢迎程度排列功能"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/621205714"
zhihu_id: "621205714"
zhihu_title: "yiduobo的每日leetcode 1772.按受欢迎程度排列功能"
question_id: "1772"
question: "按受欢迎程度排列功能"
problem_url: "https://leetcode.cn/problems/sort-features-by-popularity/"
created: "2023-04-12T01:12:49+08:00"
updated: "2023-04-12T01:12:49+08:00"
upvotes: 0
comments: 0
---

# 1772. 按受欢迎程度排列功能

> **[yiduobo的每日leetcode 1772.按受欢迎程度排列功能](https://zhuanlan.zhihu.com/p/621205714) · 知乎 · 2023-04-12 · 赞同 0**
> 力扣：[1772. 按受欢迎程度排列功能](https://leetcode.cn/problems/sort-features-by-popularity/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1772.按受欢迎程度排列功能

[力扣](https://leetcode.cn/problems/sort-features-by-popularity/)

题目要求统计features中的每个字符串在多少个response中出现过，这类字符串匹配的问题可以使用trie树来进行求解。

将features中的每个字符串都加入到trie树中，然后遍历response数组，对于每个字符串再分别遍历其中的单词，利用trie树检测该单词是否出现在trie树中，同时使用集合记录当前response中出现过哪些features中的字符串。

得到单个response对应的features集合后，再使用一个总的哈希表记录每种feature出现的次数，最后根据次数从大到小对features进行排序即可。

最后附上python代码：

```python
class TreeNode(object):

    def __init__(self):
        self.childs = {}
        self.end_id = None

class Solution(object):
    def sortFeatures(self, features, responses):
        """
        :type features: List[str]
        :type responses: List[str]
        :rtype: List[str]
        """

        root = TreeNode()

        for index, s in enumerate(features):
            now = root
            for char in s:
                if char not in now.childs:
                    node = TreeNode()
                    now.childs[char] = node
                
                now = now.childs[char]
            
            now.end_id = index
        
        cnt = [0] * len(features)
        for r in responses:
            hit_set = set()
            for s in r.split(' '):
                now = root
                flag = True
                for char in s:
                    if char not in now.childs:
                        flag = False
                        break
                    now = now.childs[char]
                
                if flag and now.end_id is not None:
                    hit_set.add(now.end_id)
            
            for id in hit_set:
                cnt[id] += 1

        return [features[x] for x in sorted(range(len(features)), key=lambda d:(-cnt[d], d))]
```
