---
title: "3569. 分割数组后不同质数的最大数目"
aliases: ["yiduobo的每日leetcode 3569.分割数组后不同质数的最大数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "leetcode/hash-table", "leetcode/math", "leetcode/number-theory", "leetcode/ordered-set", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1936229154799489811"
zhihu_id: "1936229154799489811"
zhihu_title: "yiduobo的每日leetcode 3569.分割数组后不同质数的最大数目"
question_id: "3569"
question: "分割数组后不同质数的最大数目"
problem_url: "https://leetcode.cn/problems/maximize-count-of-distinct-primes-after-split/"
difficulty: "Hard"
rating: 2697
created: "2025-08-06T01:40:48+08:00"
updated: "2025-08-06T01:40:48+08:00"
upvotes: 1
comments: 0
---

# 3569. 分割数组后不同质数的最大数目

> **[yiduobo的每日leetcode 3569.分割数组后不同质数的最大数目](https://zhuanlan.zhihu.com/p/1936229154799489811) · 知乎 · 2025-08-06 · 赞同 1**
> 力扣：[3569. 分割数组后不同质数的最大数目](https://leetcode.cn/problems/maximize-count-of-distinct-primes-after-split/) · Hard · 灵茶山艾府：[Lazy 线段树 + 有序集合，两种写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3569.分割数组后不同质数的最大数目

[3569. 分割数组后不同质数的最大数目 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-count-of-distinct-primes-after-split/)

题目给出一个长度为n的数组nums，以及一个二维查询数组queries，其中queries[index] \= [idx, val]。

对于每个查询，需要先将nums[idx]更新为val，接下来从1到n - 1之间选择一个k，将nums划分成nums[:k]以及nums[k:]，使得这两个子数组中不同质数的数量之和最大。

对于单次查询来说，直接寻找划分点感觉会比较困难。注意到对于特定的划分点c，不同质数之间相互不会产生影响，因此在这里可以从每种质数的角度出发来考虑。

对于某个质数v，不妨设当前的划分点为c。方便起见，这里不沿用上面k的定义，而是重新定义为nums[0]到nums[c]被划分到前半部分，而nums[c + 1]到nums[n - 1]被划分到后半部分，那么：

1、若v一次都没出现过：

此时c不管是什么，v都不会被计入答案

2、若v恰好出现了一次：

此时c不管是什么，v要么被划分到前半部分，要么被划分到后半部分，一定会被计入答案恰好1次

3、若v出现了多次：

此时只有当v同时被划分到两个部分中才会计入答案两次，否则同样也只会计入答案恰好1次。更进一步的，v同时被划分到两个部分中，意味着最左侧的v出现的位置必须小于等于c，而最右侧的v出现的位置必须大于c。

于是在这里可以使用两个嵌套堆的哈希表first和last记录v出现的所有位置。其中first[v]记录v出现的所有下标，这样一来first[v]的堆顶就是这些下标中的最小值，也就是最左侧的v出现的位置；相对的，last[v]记录v出现的所有下标的相反数，而这样的话last[v]的堆顶就是这些下标中的最大值，也就是最右侧的v出现的位置。

在这里之所以采用堆而不是简单的哈希表，是因为后续的修改操作可能会让最左侧和最右侧v的位置产生变化，因此在这里采用堆加上懒更新的处理方法，可以在任意时刻高效地得知v最左侧和最右侧的下标。

基于上面的描述，就可以在一开始先将nums中所有质数的下标都收集起来，接下来对于每种质数v，其至少会被计入答案一次，而当分割点位于first[v][0]到-last[v][0] - 1之间时，还会被额外计入答案一次，因此在这里可以将问题转化为给出若干条线段，问0到n - 2之间的每个点被多少条线段覆盖住。对于这个问题，只需通过差分数组记录每条线段，然后一趟遍历就可以得出初始状态下每个分割点对应的答案，取其中的最大值就是初始的最优划分对应的答案。

---

接下来处理查询。对于当前查询(idx, val)，若nums[idx]本来就等于val，此时无事发生，可以直接沿用上一轮的答案，否则的话就需要进行针对性的处理。

首先考察被移除掉的原来的nums[idx]，不妨记为rm_v。若rm_v不是质数，那么其一开始就没有对答案产生影响，将其移除后也不影响答案，反之如果rm_v为质数，此时也不会影响到其他质数对答案的贡献，只需要考虑rm_v：

1、在本次操作后rm_v在nums中不再出现：

说明rm_v之前恰好出现一次，也就是说rm_v会让答案增加1，此时将其移除则应该将答案减去1

2、本次操作移除的是最左侧的rm_v，也就是当前的下标idx小于新的first[rm_v][0]：

此时相当于将之前rm_v对应的那条线段的idx到first[rm_v][0] - 1这一段剪掉了，因此需要将分割点在idx到first[rm_v][0] - 1之间对应的答案减去1

3、本次操作移除的是最右侧的rm_v，也就是当前的下标idx大于新的-last[rm_v][0]：

与情况2对称，此时则需要将分割点在-last[rm_v][0]到idx - 1之间对应的答案减去1

4、本次操作移除的是某个处于中间的rm_v：

此时不会影响之前描述的线段，因此无需更新答案

可以发现，以上几种情况要么无需操作，要么是对某个区间加上1或者减去1，在这里可以采用懒更新的线段树来完成区间的更新。另外，无论是哪种情况，都需要更新first[rm_v]以及last[rm_v]这两个堆。

---

接下来考察新加入的val。与上面的处理方法类似，若val不是质数，那么无需处理，否则也只需要考虑idx与first[val][0]以及-last[val][0]的位置关系，来更新val对答案产生的影响：

1、在本次操作后val在nums中恰好出现一次：

说明val之前从没出现过，也就是说本次新增的val会让答案增加1

2、本次操作新增的val在原始最左侧的val的左侧，也就是idx \< first[val][0]：

此时相当于在val对应的线段左侧新增idx到first[val][0] - 1这一段，因此需要将分割点在这一段间的答案加上1

3、本次操作新增的val在原始最右侧的val的右侧，也就是idx > -last[val][0]：

与情况2对称，此时只需将-last[rm_v][0]到idx - 1之间的答案加上1

4、本次操作新的val处于原始val的中部：

此时无需更新答案

可以发现，在这里也可以通过线段树来完成区间的更新。同样的，无论是哪种情况，在这里都需要更新first[val]以及last[val]。

删除和添加都处理完成后，只需通过线段树查询对应答案最大的分割点，将其对应的答案加入到答案数组中即可。

最后附上python代码：

```python
class Solution(object):
    def maximumCount(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        ma = 100000
        prime = [True] * (ma + 1)
        prime[1] = False

        for v in range(2, ma + 1):
            if prime[v]:
                for x in range(v + v, ma + 1, v):
                    prime[x] = False

        first = {}
        last = {}
        n = len(nums)
        for index, v in enumerate(nums):
            if prime[v]:
                if v not in first:
                    first[v] = [index]
                    last[v] = [-index]
                else:
                    heapq.heappush(first[v], index)
                    heapq.heappush(last[v], -index)

        d = [0] * n
        for v in first:
            d[first[v][0]] += 1
            d[-last[v][0]] -= 1

        cnt = len(first)
        f = [0] * (n * 4)
        delta = [0] * (n * 4)
        ori = [0] * n

        def build(now, left, right):
            if left == right:
                f[now] = ori[left]
                return
            
            mid = (left + right) >> 1
            left_child = now + now + 1
            right_child = now + now + 2
            build(left_child, left, mid)
            build(right_child, mid + 1, right)
            f[now] = max(f[left_child], f[right_child])

        def update(now, left, right, start, end, v):
            if left == start and right == end:
                delta[now] += v
                return
            
            left_child = now + now + 1
            right_child = now + now + 2

            mid = (left + right) >> 1
            if end <= mid:
                update(left_child, left, mid, start, end, v)
            elif start > mid:
                update(right_child, mid + 1, right, start, end, v)
            else:
                update(left_child, left, mid, start, mid, v)
                update(right_child, mid + 1, right, mid + 1, end, v)
            
            f[now] = max(f[left_child] + delta[left_child], f[right_child] + delta[right_child])

        
        for index in range(n - 1):
            cnt += d[index]
            ori[index] = cnt

        build(0, 0, n - 2)
        
        res = []
        for index, v in queries:
            if nums[index] == v:
                res.append(f[0] + delta[0])
                continue
            
            rm_v = nums[index]
            if prime[rm_v]:
                while first[rm_v] and (nums[first[rm_v][0]] != rm_v or first[rm_v][0] == index):
                    heapq.heappop(first[rm_v])
                while last[rm_v] and (nums[-last[rm_v][0]] != rm_v or -last[rm_v][0] == index):
                    heapq.heappop(last[rm_v])

                if not first[rm_v]:
                    update(0, 0, n - 2, 0, n - 2, -1)
                elif index < first[rm_v][0]:
                    update(0, 0, n - 2, index, first[rm_v][0] - 1, -1)
                elif index > -last[rm_v][0]:
                    update(0, 0, n - 2, -last[rm_v][0], index - 1, -1)
            
            if prime[v]:
                if v not in first:
                    first[v] = []
                    last[v] = []

                while first[v] and nums[first[v][0]] != v:
                    heapq.heappop(first[v])
                while last[v] and nums[-last[v][0]] != v:
                    heapq.heappop(last[v])
                
                if not first[v]:
                    update(0, 0, n - 2, 0, n - 2, 1)
                elif index < first[v][0]:
                    update(0, 0, n - 2, index, first[v][0] - 1, 1)
                elif index > -last[v][0]:
                    update(0, 0, n - 2, -last[v][0], index - 1, 1)
                
                heapq.heappush(first[v], index)
                heapq.heappush(last[v], -index)
            
            nums[index] = v
            res.append(f[0] + delta[0])
        
        return res
```
