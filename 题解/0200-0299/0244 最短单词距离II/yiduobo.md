---
title: "244. 最短单词距离II"
aliases: ["yiduobo的每日leetcode 244.最短单词距离II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/591642641"
zhihu_id: "591642641"
zhihu_title: "yiduobo的每日leetcode 244.最短单词距离II"
question_id: "244"
question: "最短单词距离II"
problem_url: "https://leetcode.cn/problems/shortest-word-distance-ii/"
created: "2022-12-14T04:10:56+08:00"
updated: "2022-12-14T04:10:56+08:00"
upvotes: 0
comments: 0
---

# 244. 最短单词距离II

> **[yiduobo的每日leetcode 244.最短单词距离II](https://zhuanlan.zhihu.com/p/591642641) · 知乎 · 2022-12-14 · 赞同 0**
> 力扣：[244. 最短单词距离II](https://leetcode.cn/problems/shortest-word-distance-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

244.最短单词距离II

[力扣](https://leetcode.cn/problems/shortest-word-distance-ii/)

之前243题的多次调用版本，那么很自然想到记录下之前查询过的单词对，防止极限数据下每次询问都盯着一对单词使劲薅。

最直观的做法自然是照搬243题的算法执行多次，但是243题的算法时间复杂度为O(n)，即使使用缓存储存之前请求的结果，也还是有办法通过构造测试数据来使得每次请求的时间复杂度保持在O(n)，那么总体的复杂度就是O(nq)，这个复杂度在本体的数据规模下是有风险的。

另一种想法就是利用出现位置的有序性，通过二分来计算最终答案。具体来说就是遍历出现次数较少的单词的所有下标位置p，然后在另一个单词出现位置数组中二分这个p，找到与p最接近的1个或2个位置然后计算距离。

对于这种算法，在最坏情况下应该是所有单词出现次数都很接近，因为每次询问都是遍历较短的位置序列，只有两个位置序列长度接近时才能保证时间复杂度最高。另一方面，由于cache的存在，那么必须构造出q中不同的询问。m个单词能提供的不同请求数目就是C(m, 2) \= m \* (m - 1) / 2，这个值等于q，那么m就是sqrt(q)这个量级的。此时的时间复杂度就是O(q \* (n / m) \* log(n / m))，前面的q \* (n / m)可以认为是sqrt(q) \* n，而log里的内容可以直接取更大的log(n)，那么最终的时间复杂度不会超过O(sqrt(q) \* nlog(n))，完全是可行的。

最后附上python代码：

```python
class WordDistance(object):

    def __init__(self, wordsDict):
        """
        :type wordsDict: List[str]
        """
        self.words_pos = {}
        self.pair_cache = {}

        for index, word in enumerate(wordsDict):
            if word not in self.words_pos:
                self.words_pos[word] = []
            self.words_pos[word].append(index)

    def shortest(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: int
        """
        if word1 < word2:
            key = word1 + '|' + word2
        else:
            key = word2 + '|' + word1
        
        if key in self.pair_cache:
            return self.pair_cache[key]
        
        if len(self.words_pos[word1]) <= len(self.words_pos[word2]):
            pos_list1 = self.words_pos[word1]
            pos_list2 = self.words_pos[word2]
        else:
            pos_list1 = self.words_pos[word2]
            pos_list2 = self.words_pos[word1]

        res = None

        for p in pos_list1:
            if p <= pos_list2[0]:
                tmp = pos_list2[0] - p
            elif p >= pos_list2[-1]:
                tmp = p - pos_list2[-1]
            else:
                left = 0
                right = len(pos_list2) - 1
                while left < right:
                    mid = (left + right) >> 1
                    if pos_list2[mid] >= p:
                        right = mid
                    else:
                        left = mid + 1
                
                tmp = min(pos_list2[left] - p, p - pos_list2[left - 1])
            
            if res is None or res > tmp:
                res = tmp
        
        self.pair_cache[key] = res
        return res

# Your WordDistance object will be instantiated and called as such:
# obj = WordDistance(wordsDict)
# param_1 = obj.shortest(word1,word2)
```
