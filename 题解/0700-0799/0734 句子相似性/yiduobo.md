---
title: "734. 句子相似性"
aliases: ["yiduobo的每日leetcode 734.句子相似性"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/605310071"
zhihu_id: "605310071"
zhihu_title: "yiduobo的每日leetcode 734.句子相似性"
question_id: "734"
question: "句子相似性"
problem_url: "https://leetcode.cn/problems/sentence-similarity/"
created: "2023-02-10T23:30:39+08:00"
updated: "2023-02-10T23:30:39+08:00"
upvotes: 0
comments: 0
---

# 734. 句子相似性

> **[yiduobo的每日leetcode 734.句子相似性](https://zhuanlan.zhihu.com/p/605310071) · 知乎 · 2023-02-10 · 赞同 0**
> 力扣：[734. 句子相似性](https://leetcode.cn/problems/sentence-similarity/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

734.句子相似性

[力扣](https://leetcode.cn/problems/sentence-similarity/)

由于题目中的相似关系是固定的单词对，那么可以使用哈希表将所有相似的词对储存起来，然后就可以高效判断两个单词是否相似了。在这里需要注意的是，若x和y相似，那么y也和x相似，需要分别储存。如果想只储存一组，那么就需要保证x和y的有序性。

接下来进行判断。

若两个数组长度不相同，那么直接返回false。否则逐对遍历数组中的单词，若两个单词不相同，且组成的词对没有出现在哈希表中，那么就返回false。若成功遍历完数组，那么返回true。

具体实现上，可以先建立单词到数字id的映射，然后通过id而不是字符串来进行具体操作，效率相对会高一些。

最后附上python代码：

```python
class Solution(object):
    def areSentencesSimilar(self, sentence1, sentence2, similarPairs):
        """
        :type sentence1: List[str]
        :type sentence2: List[str]
        :type similarPairs: List[List[str]]
        :rtype: bool
        """

        if len(sentence1) != len(sentence2):
            return False

        words_mapping = {}
        similar_set = set()
        id = 0
        for x, y in similarPairs:
            if x not in words_mapping:
                words_mapping[x] = id
                id += 1
            if y not in words_mapping:
                words_mapping[y] = id
                id += 1

            x_id, y_id = words_mapping[x], words_mapping[y]
            if x_id > y_id:
                x_id, y_id = y_id, x_id
            similar_set.add((x_id, y_id))

        for x, y in zip(sentence1, sentence2):
            if x == y:
                continue
            
            x_id, y_id = words_mapping.get(x, -1), words_mapping.get(y, -1)
            if x_id > y_id:
                x_id, y_id = y_id, x_id
            if (x_id, y_id) not in similar_set:
                return False
        
        return True
```
