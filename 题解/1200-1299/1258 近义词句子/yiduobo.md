---
title: "1258. 近义词句子"
aliases: ["yiduobo的每日leetcode 1258.近义词句子"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/615023082"
zhihu_id: "615023082"
zhihu_title: "yiduobo的每日leetcode 1258.近义词句子"
question_id: "1258"
question: "近义词句子"
problem_url: "https://leetcode.cn/problems/synonymous-sentences/"
created: "2023-03-18T14:45:46+08:00"
updated: "2023-03-18T14:45:46+08:00"
upvotes: 0
comments: 0
---

# 1258. 近义词句子

> **[yiduobo的每日leetcode 1258.近义词句子](https://zhuanlan.zhihu.com/p/615023082) · 知乎 · 2023-03-18 · 赞同 0**
> 力扣：[1258. 近义词句子](https://leetcode.cn/problems/synonymous-sentences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1258.近义词句子

[力扣](https://leetcode.cn/problems/synonymous-sentences/)

通过样例可以观察到，题目中的近义词是可以传递的，比如说happy \<-> joy \<-> cheerful，在最终替换时也可以用cheerful来替换happy。也就是说，在这里需要使用维护各个单词间的连通性，最直观的处理方法就是使用并查集。

得到单词间的连通性之后，需要再遍历所有单词，将这些单词按其最上层的父节点收集起来并排序。

最后，则需要使用搜索回溯来找出所有可能形成的句子。具体来说，就是逐个单词向后搜索，对于当前单词，若其出现在并查集中，那么就逐个尝试上一步中已经排好序的单词然后进行下一步的搜索回溯。

最后附上python代码：

```python
class Solution(object):
    def generateSentences(self, synonyms, text):
        """
        :type synonyms: List[List[str]]
        :type text: str
        :rtype: List[str]
        """

        word_mapping = {}
        cnt = 0
        for x, y in synonyms:
            if x not in word_mapping:
                word_mapping[x] = cnt
                cnt += 1
            
            if y not in word_mapping:
                word_mapping[y] = cnt
                cnt += 1
        
        fa = range(cnt)

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        for x, y in synonyms:
            x_id = word_mapping[x]
            y_id = word_mapping[y]

            fa_x = find(x_id)
            fa_y = find(y_id)

            if fa_x != fa_y:
                fa[fa_x] = fa_y
        
        syn_dict = {}
        for word in word_mapping:
            fa_word = find(word_mapping[word])
            if fa_word not in syn_dict:
                syn_dict[fa_word] = []
            syn_dict[fa_word].append(word)
        
        for fa_word in syn_dict:
            syn_dict[fa_word].sort()
        
        res = []
        word_list = text.split(' ')
        n = len(word_list)

        def dfs(level, now):
            if level == n:
                res.append(' '.join(now))
                return
            
            if word_list[level] in word_mapping:
                fa_word = find(word_mapping[word_list[level]])
                for syn_word in syn_dict[fa_word]:
                    now.append(syn_word)
                    dfs(level + 1, now)
                    now.pop()
            else:
                now.append(word_list[level])
                dfs(level + 1, now)
                now.pop()
        
        dfs(0, [])
        return res
```
