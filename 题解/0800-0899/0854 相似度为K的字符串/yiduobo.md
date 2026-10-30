---
title: "854. 相似度为K的字符串"
aliases: ["yiduobo的每日leetcode 854.相似度为K的字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/348904839"
zhihu_id: "348904839"
zhihu_title: "yiduobo的每日leetcode 854.相似度为K的字符串"
question_id: "854"
question: "相似度为K的字符串"
problem_url: "https://leetcode.cn/problems/k-similar-strings/"
created: "2021-02-04T21:27:03+08:00"
updated: "2021-02-04T21:27:03+08:00"
upvotes: 1
comments: 0
---

# 854. 相似度为K的字符串

> **[yiduobo的每日leetcode 854.相似度为K的字符串](https://zhuanlan.zhihu.com/p/348904839) · 知乎 · 2021-02-04 · 赞同 1**
> 力扣：[854. 相似度为K的字符串](https://leetcode.cn/problems/k-similar-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

854.相似度为K的字符串

[力扣](https://leetcode-cn.com/problems/k-similar-strings/)

首先，对于已经匹配的字母，显然是没有进行交换的必要。

接下来，对于一个参与字母数量为k的交换序列，需要花费k - 1次操作进行交换。例如样例2中的abc和bca，其中唯一的一个交换序列为a -> c -> b -> a，有3个字母参与了交换，因此完成交换需要两次操作。

那么假设我们需要交换的字母一共有m个，最终分成了n组交换序列，每一组交换序列包含的字符数量分别为C1, C2, ..., Cn，那么最终需要的操作数ans一共就是

(C1 - 1) + (C2 - 1) + ... + (Cn - 1) \= (C1 + C2 + ... + Cn) - n \= m - n。

为了让ans尽可能小，那么我们需要构造出尽可能多的交换序列使得n尽可能大。注意到这里的字符只有a到f，因此可以通过状态压缩动态规划来解决。

由于这里出现的字符只有a到f，因此最终的交换序列中可能出现的字符数量也只有2-6这几种情况。枚举所有可能出现的交换序列，并统计每个交换序列将产生的字符交换。例如对于样例2中的acb，这就是一个3个字符的序列，其中将产生a -> c、c -> b以及b -> a这三种字符交换。另外需要注意的是，某些交换序列虽然字符排布不同，但本质是一样的，例如bac，其产生的三种字符交换是b -> a、a -> c以及c -> b，与上面的acb相同。为了去重，一个简单的做法就是将序列中最小的字符轮转到最前面，例如bac，我们将a轮转到最前面之后就变成了acb，这样一来就可以高效去重了。

枚举出所有可行的交换序列后，将其储存在一个dict中，然后统计从A到B当中存在多少可用的字符交换。所谓可用的字符交换就是指当A[index]与B[index]不同时，我们需要将A[index]变成B[index]，因此存在一个A[index] -> B[index]的字符交换。

统计完成后，将初始可用的字符交换作为初始状态开始进行动态规划。每次枚举所有可行的交换序列，若当前剩下的可用的字符交换state可以覆盖到当前的枚举到的交换序列candidate，那么就有f\[state\] \= max(f\[state\], f\[state - swap\[candidate\]\] + 1)，其中swap\[candidate\]表示交换序列candidate中使用了哪些字符交换。边界条件为所有边都用完时f值为0。

得益于python强劲的哈希表，我最终直接使用的tuple，并没有进行显式的状态压缩。具体来说就是使用list统计剩余每条边出现的数量，然后将其转化为tuple进行动态规划。

最后附上python代码：

```python
class Solution(object):
    def kSimilarity(self, A, B):
        """
        :type A: str
        :type B: str
        :rtype: int
        """

        edge_dict = {}
        cnt = 0
        for x in ['a', 'b', 'c', 'd', 'e', 'f']:
            for y in ['a', 'b', 'c', 'd', 'e', 'f']:
                if x != y:
                    key = x + y
                    edge_dict[key] = cnt
                    cnt += 1

        q = ['a', 'b', 'c', 'd', 'e', 'f']
        l = 0
        r = 6
        circle_dict = {}
        length = 1
        while length < 6:
            length += 1
            for now in q[l:r]:
                for char in ['a', 'b', 'c', 'd', 'e', 'f']:
                    if now.find(char) == -1:
                        tmp = now + char
                        min_pos = 0
                        for index in range(1, len(tmp)):
                            if tmp[index] < tmp[min_pos]:
                                min_pos = index
                        tmp = tmp[min_pos:] + tmp[:min_pos]
                        if tmp not in circle_dict:
                            circle_dict[tmp] = [edge_dict[tmp[index] + tmp[(index + 1) % length]] for index in range(length)]
                            q.append(tmp)
            
            l, r = r, len(q)

        f = {}
        edge_list = [0] * len(edge_dict)
        f[tuple(edge_list)] = 0
        for index in range(len(A)):
            if A[index] != B[index]:
                key = A[index] + B[index]
                edge_list[edge_dict[key]] += 1

        return sum(edge_list) - self.dfs(tuple(edge_list), circle_dict, f)
    
    def dfs(self, now, circle_dict, f):
        if now not in f:
            f[now] = -1
            for circle in circle_dict:
                tmp = list(now)
                flag = True
                for edge in circle_dict[circle]:
                    if tmp[edge] > 0:
                        tmp[edge] -= 1
                    else:
                        flag = False
                        break
                if flag:
                    f[now] = max(f[now], 1 + self.dfs(tuple(tmp), circle_dict, f))
        
        return f[now]
```
