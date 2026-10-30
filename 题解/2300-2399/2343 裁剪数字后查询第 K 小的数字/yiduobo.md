---
title: "2343. 裁剪数字后查询第K小的数字"
aliases: ["yiduobo的每日leetcode 2343.裁剪数字后查询第K小的数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/sorting", "leetcode/chi-xian-suan-fa", "题单/常用数据结构", "题单/常用数据结构/专题-离线算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/560399164"
zhihu_id: "560399164"
zhihu_title: "yiduobo的每日leetcode 2343.裁剪数字后查询第K小的数字"
question_id: "2343"
question: "裁剪数字后查询第 K 小的数字"
problem_url: "https://leetcode.cn/problems/query-kth-smallest-trimmed-number/"
difficulty: "Medium"
rating: 1652
created: "2022-09-02T02:36:01+08:00"
updated: "2022-09-02T02:36:01+08:00"
upvotes: 0
comments: 0
---

# 2343. 裁剪数字后查询第K小的数字

> **[yiduobo的每日leetcode 2343.裁剪数字后查询第K小的数字](https://zhuanlan.zhihu.com/p/560399164) · 知乎 · 2022-09-02 · 赞同 0**
> 力扣：[2343. 裁剪数字后查询第 K 小的数字](https://leetcode.cn/problems/query-kth-smallest-trimmed-number/) · Medium · 灵茶山艾府：[两种做法：直接排序 / 离线+增量排序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2343.裁剪数字后查询第K小的数字

[力扣](https://leetcode.cn/problems/query-kth-smallest-trimmed-number/)

题目中描述的裁剪数字的过程与经典的基数排序非常像，那么当然就应该用基数排序来预处理出数组在每一种裁剪情况下的大小顺序了。

接下来描述一下基数排序的具体执行过程。

对于本题，需要使用一个数组rank来记录每一轮的排序结果，即rank[i]为截取了最后i位的排序结果。rank[0]初始化为0到n - 1。

接下来，从1到m遍历每一个数位，每一轮都设置10个桶，这些桶都初始化为空的list。对于当前遍历到的数位rnd，从0开始到n - 1遍历rank[rnd - 1]。

这里需要特别注意，必须是从小到大遍历rank\[rnd - 1\]。对于当前遍历到的数rank\[rnd - 1\]\[index\]，记录的是一个下标值，对应的具体数字为num\[rank\[rnd - 1\]\[index\]\]。将其倒数第rnd位分离出来，记为digit。接下来将rank\[rnd - 1\]\[index\]加入到digit对应桶中的list末尾即可。

全部遍历完成后，从按下标0到9遍历这10个桶，然后将桶中的数按顺序添加到rank[rnd]的末尾。也就是说，此时最后rnd位的排序已经完成了。

这样做可以排序的理由是，对于所有数的最后rnd位，比较大小显然是先看倒数第rnd位，也就是用来选择桶的数digit。在这里可以发现，不同的digit就已经通过分桶的不同确定了大小关系。

接下来对于相同的digit，则需要比较的就是后rnd - 1位的大小，而这个大小恰好就是rank[rnd - 1]中的顺序关系，因此在前面强调必须按顺序遍历rank[rnd - 1]，保证了在digit相同时，后rnd - 1位较小的数会由于先遍历到，所以先加入digit对应的桶中，这样一来最后按顺序将所有桶中的数收集起来时，较小的数就会因为先收集到所以排在更前面了。

按照上面描述的过程计算得到每一轮的rank后，就只需遍历queries，去rank中查找对应的结果即可。

最后附上python代码：

```python
class Solution(object):
    def smallestTrimmedNumbers(self, nums, queries):
        """
        :type nums: List[str]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        n = len(nums)
        rank = [range(n)]
        order = [range(n)]

        m = len(nums[0])

        for rnd in range(1, m + 1):
            bin_list = [[] for _ in range(10)]
            for r in rank[-1]:
                digit = int(nums[r][-rnd])
                bin_list[digit].append(r)
            
            rank.append([])
            for digit in range(0, 10):
                rank[-1].extend(bin_list[digit])

        res = [rank[trim][k - 1] for k, trim in queries]
        
        return res
```
