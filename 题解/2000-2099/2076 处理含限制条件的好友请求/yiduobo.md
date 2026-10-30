---
title: "2076. 处理含限制条件的好友请求"
aliases: ["yiduobo的每日leetcode 2076.处理含限制条件的好友请求"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/union-find", "leetcode/hash-table", "题单/常用数据结构", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/517098610"
zhihu_id: "517098610"
zhihu_title: "yiduobo的每日leetcode 2076.处理含限制条件的好友请求"
question_id: "2076"
question: "处理含限制条件的好友请求"
problem_url: "https://leetcode.cn/problems/process-restricted-friend-requests/"
difficulty: "Hard"
rating: 2131
created: "2022-05-19T22:21:01+08:00"
updated: "2022-05-19T22:21:01+08:00"
upvotes: 0
comments: 0
---

# 2076. 处理含限制条件的好友请求

> **[yiduobo的每日leetcode 2076.处理含限制条件的好友请求](https://zhuanlan.zhihu.com/p/517098610) · 知乎 · 2022-05-19 · 赞同 0**
> 力扣：[2076. 处理含限制条件的好友请求](https://leetcode.cn/problems/process-restricted-friend-requests/) · Hard · 灵茶山艾府：[O(nlogn) 做法：用并查集维护朋友关系，同时用哈希表维护代表元之间能否成为朋友](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2076.处理含限制条件的好友请求

[力扣](https://leetcode.cn/problems/process-restricted-friend-requests/)

对于本题从图的角度出发，可以将每个人视为图中的一个点，两个人之间的关系视为图中的一条边。题目给出若干点对，要求这些点对在图中不允许连通，然后再给出若干询问，问如果将询问中的点对连上边，是否会使得之前不允许联通的点对变成连通，若不是，那么就将询问中的点对连上边。

对于这类动态的连通性相关的问题，很自然想到使用并查集来处理。

依次枚举每一组询问，对于当前询问中的点对x、y，使用并查集找到这两个点的祖先节点fa_x、fa_y。接下来枚举restrictions中每一组点对u、v，同样求出这两个点的祖先节点fa_u和fa_v，若fa_x等于fa_u且fa_y等于fa_v，或者反过来fa_x等于fa_v，fa_y等于fa_u，那么将x和y连通后会使得u和v也连通，说明x和y是不能连通的。若不存在点对u、v满足上面的条件，那么说明x和y可以连通，此时利用fa_x和fa_y更新x和y的连通性即可。

最后附上python代码：

```python
class Solution(object):
    def friendRequests(self, n, restrictions, requests):
        """
        :type n: int
        :type restrictions: List[List[int]]
        :type requests: List[List[int]]
        :rtype: List[bool]
        """

        fa = range(n)

        def find(x):
            if x != fa[x]:
                fa[x] = find(fa[x])
            
            return fa[x]

        res = []
        for x, y in requests:
            fa_x = find(x)
            fa_y = find(y)
            if fa_x == fa_y:
                res.append(True)
            else:
                flag = True
                for u, v in restrictions:
                    fa_u = find(u)
                    fa_v = find(v)
                    if (fa_x == fa_u and fa_y == fa_v) or (fa_x == fa_v and fa_y == fa_u):
                        flag = False
                        break
                
                if flag:
                    fa[fa_x] = fa_y
                    res.append(True)
                else:
                    res.append(False)

        return res
```
