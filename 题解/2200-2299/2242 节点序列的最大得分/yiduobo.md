---
title: "2242. 节点序列的最大得分"
aliases: ["yiduobo的每日leetcode 2242.节点序列的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/graph", "leetcode/brainteaser", "leetcode/enumeration", "leetcode/sorting", "题单/常用数据结构", "题单/图论算法", "题单/常用数据结构/零-常用枚举技巧", "题单/图论算法/九-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/545403943"
zhihu_id: "545403943"
zhihu_title: "yiduobo的每日leetcode 2242.节点序列的最大得分"
question_id: "2242"
question: "节点序列的最大得分"
problem_url: "https://leetcode.cn/problems/maximum-score-of-a-node-sequence/"
difficulty: "Hard"
rating: 2304
created: "2022-07-24T01:23:41+08:00"
updated: "2022-07-24T01:23:41+08:00"
upvotes: 0
comments: 0
---

# 2242. 节点序列的最大得分

> **[yiduobo的每日leetcode 2242.节点序列的最大得分](https://zhuanlan.zhihu.com/p/545403943) · 知乎 · 2022-07-24 · 赞同 0**
> 力扣：[2242. 节点序列的最大得分](https://leetcode.cn/problems/maximum-score-of-a-node-sequence/) · Hard · 灵茶山艾府：[一步步提示如何做出此题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2242.节点序列的最大得分

[力扣](https://leetcode.cn/problems/maximum-score-of-a-node-sequence/)

乍一看感觉还蛮难的，不过题目非常好心地设置了只需要找出长度为4的序列中的最大得分，那么可以从这个4入手来想办法。

长度为4的序列拉直，就可以写成

p - x - y - q

由于题目的数据规模比较大，必须使用O(n)或者O(nlogn)的算法才行，也就是只有一次枚举遍历的机会。对于这类问题，例如之前遇到的山峰山谷等，通常的做法就是枚举中间这一项，然后想办法求出在这种情况下两边的最优解。本题也是一样，可以先枚举x - y这一条边，那么问题就变成了找出一组p和q，使得p和q的得分最大，且p和q不能重复。

由于必须存在p和q才能让这个序列长度为4，因此x和y必须至少与两个点相连。即x与p、y相连，y与x、q相连。另一方面，由于与某个节点相邻的节点数目可能非常多，但是实际上只需要找出其中最大的，因此可以先预处理出与每个节点相邻的最大的两个节点。

但是在这里还有一种特殊情况是与x相邻的除y之外的最大节点p1，和与y相邻的除x之外的最大节点q1，是同一个节点，那么这种情况也是不合法的。这种情况可以参考样例1中，当x \= 1，y \= 2时，此时的p1和q1都是3，这是不合法的，此时就需要使用p2 \= 0或q2 \= 4来替代p1或q1其中一项，才能得到合法的长度为4的序列。换言之，预处理的时候就需要找出与每个节点相邻的最大的三个节点。当然，如果找不到也不能强求。

分别记与节点x相邻的最大、次大、第三大的节点为first[x], second[x], third[x]，然后开始枚举x - y：

1、若second[x]或second[y]为空，说明x或y只与一个点相连，那么必然凑不出长度为4的序列，因此可以直接跳过x - y这种情况

2、若third[x]为空，那么p只有一种选择。当first[x] \= y时，p就是second[x]，否则p就是first[x]：

2-1）若third[y]也为空，那么同样的，q也只有一种选择。

当first[y] \= x时，q就是second[y]，否则q就是first[y]。此时得到了一组p和q，若p \= q，那么说明此时凑不出长度为4的序列，否则就是用p - x - y - q来更新答案。

2-2）若third[y]不为空，那么说明当最理想的q与p重复时，有备选的q可以使用从而一定能凑出长度为4的序列：

2-2-1）当first[y] \= x且second[y] \= p时，可以取q \= third[y]

2-2-2）当first[y] \= x且second[y] !\= p时，可以取q \= second[y]

2-2-3）当first[y] \= p且second[y] \= x时，可以取q \= third[y]

2-2-4）当first[y] \= p且second[y] !\= x时，可以取q \= second[y]

2-2-5）其他情况下，都可以取q \= first[y]

这样一来，总是能得到合法的p - x - y - q，使用这个结果更新答案。

3、若third[x]不为空，且third[y]为空，那么此时与情况2完全对称，先找到唯一的q，再按具体情况对照2-2）中的操作找出对应的p即可。

4、若third[x]和third[y]都不为空，说明p和q都有多种选择。当最优的p和q相同时，则可以考虑最优p加上备选q，或者备选p加上最优q的组合：

若first[x] \= y，那么最优p和备选p分别为p1 \= second[x], p2 \= third[x]

若second[x] \= y，那么最优p和备选p分别为p1 \= first[x], p2 \= third[x]

其他情况下，最优p和备选p就是p1 \= first[x], p2 \= second[x]

同样的，按相同的逻辑找出最优q和备选q，记为q1和q2。

若p1与q1不同，那么就可以使用p1 - x - y - q1来更新答案，否则就需要从p2 - x - y - q1和p1 - x - y - q2中选择较大的一项来更新答案。

最后附上python代码：

```python
class Solution(object):
    def maximumScore(self, scores, edges):
        """
        :type scores: List[int]
        :type edges: List[List[int]]
        :rtype: int
        """

        n = len(scores)
        first = [None] * n
        second = [None] * n
        third = [None] * n

        for x, y in edges:
            if first[x] is None or scores[first[x]] < scores[y]:
                first[x], second[x], third[x] = y, first[x], second[x]
            elif second[x] is None or scores[second[x]] < scores[y]:
                second[x], third[x] = y, second[x]
            elif third[x] is None or scores[third[x]] < scores[y]:
                third[x] = y
            
            if first[y] is None or scores[first[y]] < scores[x]:
                first[y], second[y], third[y] = x, first[y], second[y]
            elif second[y] is None or scores[second[y]] < scores[x]:
                second[y], third[y] = x, second[y]
            elif third[y] is None or scores[third[y]] < scores[x]:
                third[y] = x
        
        res = -1
        for x, y in edges:
            if second[x] is None or second[y] is None:
                continue
            
            if third[x] is None:
                if first[x] == y:
                    p = second[x]
                else:
                    p = first[x]

                if third[y] is None:
                    if first[y] == x:
                        q = second[y]
                    else:
                        q = first[y]
                    
                    if p == q:
                        continue
                    else:
                        res = max(res, scores[x] + scores[y] + scores[p] + scores[q])
                else:
                    if first[y] == x:
                        if second[y] == p:
                            q = third[y]
                        else:
                            q = second[y]
                    elif first[y] == p:
                        if second[y] == x:
                            q = third[y]
                        else:
                            q = second[y]
                    else:
                        q = first[y]
                    
                    res = max(res, scores[x] + scores[y] + scores[p] + scores[q])
            
            elif third[y] is None:
                if first[y] == x:
                    q = second[y]
                else:
                    q = first[y]
                
                if first[x] == y:
                    if second[x] == q:
                        p = third[x]
                    else:
                        p = second[x]
                elif first[x] == q:
                    if second[x] == y:
                        p = third[x]
                    else:
                        p = second[x]
                else:
                    p = first[x]
                
                res = max(res, scores[x] + scores[y] + scores[p] + scores[q])
            
            else:
                if first[x] == y:
                    p1, p2 = second[x], third[x]
                elif second[x] == y:
                    p1, p2 = first[x], third[x]
                else:
                    p1, p2 = first[x], second[x]
                
                if first[y] == x:
                    q1, q2 = second[y], third[y]
                elif second[y] == x:
                    q1, q2 = first[y], third[y]
                else:
                    q1, q2 = first[y], second[y]
                
                if p1 != q1:
                    res = max(res, scores[x] + scores[y] + scores[p1] + scores[q1])
                else:
                    res = max(res, scores[x] + scores[y] + scores[p1] + scores[q2], scores[x] + scores[y] + scores[p2] + scores[q1])
        
        return res
```
