---
title: "1840. 最高建筑高度"
aliases: ["yiduobo的每日leetcode 1840.最高建筑高度"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/469691493"
zhihu_id: "469691493"
zhihu_title: "yiduobo的每日leetcode 1840.最高建筑高度"
question_id: "1840"
question: "最高建筑高度"
problem_url: "https://leetcode.cn/problems/maximum-building-height/"
difficulty: "Hard"
rating: 2374
created: "2022-02-20T00:16:33+08:00"
updated: "2022-02-20T00:16:34+08:00"
upvotes: 0
comments: 0
---

# 1840. 最高建筑高度

> **[yiduobo的每日leetcode 1840.最高建筑高度](https://zhuanlan.zhihu.com/p/469691493) · 知乎 · 2022-02-20 · 赞同 0**
> 力扣：[1840. 最高建筑高度](https://leetcode.cn/problems/maximum-building-height/) · Hard · 灵茶山艾府：[两次扫描，传播约束（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1840.最高建筑高度

[力扣](https://leetcode-cn.com/problems/maximum-building-height/)

题目n的规模非常大，直接杜绝了一趟扫描求解这种做法，只能想办法从建筑限高上入手，然后通过限高建筑实际的最大高度来反推答案。

由于题目要求相邻建筑之间的高度差最多为1，因此某一栋建筑的理论最大高度除了受到自身以及相邻建筑最大高度的影响之外，还可能受到远方建筑最大高度的影响。

例如在位置5的建筑的限高为5，位置4的建筑的限高为4，本来是合理的，但是如果此时位置3的建筑限高为2，那么将会使得位置4的建筑实际最大高度变为3，从而影响到远方位置5的建筑的限高从5变成4。

由于只会是较矮的建筑影响到较高建筑的最大高度，因此一个自然的想法就是每次选出剩余建筑中理论高度最矮的建筑。对于这栋建筑而言，其实际的最高高度就是当前的理论最高高度。接下来，若该建筑左右两侧建筑的理论高度比该建筑要高，那么就可能出现由于该建筑太矮从而影响到两侧建筑的最高高度，此时就应该使用当前建筑的高度以及其与左右两侧建筑的距离来更新左右两侧建筑的理论高度。

重复此过程，直到所有建筑都被更新过。

具体求解时，除了题目给出的限高之外，还需要额外加入位置1的建筑限高为0，以及假定的右边界位置n + 1的建筑限高为n。

由于每次都需要选出剩余建筑中理论高度最小的建筑，因此很自然想到使用堆来维护这些建筑。不过在这里除了普通的最小值之外，还涉及到了定点更新操作，因此需要自己手动实现这个堆。除了正常的功能之外，需要一个额外的数组pos记录当前建筑在堆数组中的下标，从而可以及时更新建筑的理论高度，并调整其在堆中位置。

堆相关的操作具体实现起来思路也比较简单，可能会有部分重复的代码，我在这里也没有将其封装起来。

得到所有建筑的理论最高高度之后，就需要想办法求解答案。

不妨设现在有两栋相邻的限高建筑，其位置分别为p1和p2，对应的限高分别为h1和h2。在这里先假定p1 \< p2，而h1和h2的相对高度则不做限制。

对于这两栋建筑而言，理想的模型是倒v形的，即从p1的高度h1开始逐渐向上攀升，到达某个max_h之后再逐步回落，直到p2的高度h2。

在这里可操作的空间为p2 - p1 - 1，那么一个简单的思路是先将h1和h2的高度弄到一致，然后将剩下可操作性的空间对半平分得到最终的max_h。在这里的高度差为abs(h1 - h2) - 1，那么实际上剩余的操作空间为p2 - p1 - abs(h1 - h2)，将这些操作空间对半分，就有

max_h \= max(h1, h2) + (p2 - p1 - abs(h1 - h2)) / 2

通过上面的公式计算出所有相邻限高建筑之间的最高建筑高度，然后取最大值作为答案返回即可。在这里需要特别注意的是，如果前面为了方便计算加入了位置n + 1的建筑，那么在计算最终高度时需要特别处理，因为在这里位置n + 1的建筑是不存在的。

最后附上python代码：

```python
class Solution(object):
    def maxBuilding(self, n, restrictions):
        """
        :type n: int
        :type restrictions: List[List[int]]
        :rtype: int
        """

        prev = {}
        next = {}
        p_order = [1] + sorted([p for p, h in restrictions]) + [n + 1]
        for index in range(len(p_order)):
            if index > 0:
                prev[p_order[index]] = p_order[index - 1]
            if index < len(p_order) - 1:
                next[p_order[index]] = p_order[index + 1]

        heap = sorted([[h, p] for p, h in restrictions] + [[0, 1], [n, n + 1]], key=lambda d:d[0])
        pos = {}
        limit = {}
        for index in range(len(heap)):
            pos[heap[index][1]] = index
            limit[heap[index][1]] = None

        while len(heap) > 1:
            h, p = heap[0]
            limit[p] = h

            heap[0] = heap[-1]
            heap.pop()
            now = 0
            m = len(heap)
            #堆中删除操作，将要删除的位置now与堆数组末尾进行交换并从数组末尾删去
            while True: #调整新的now在堆中的位置
                left = now + now + 1
                left_flag = left < m and heap[left][0] < heap[now][0]
                
                right = now + now + 2
                right_flag = right < m and heap[right][0] < heap[now][0]

                if left_flag:
                    if right_flag:
                        if heap[left][0] < heap[right][0]:
                            heap[now], heap[left] = heap[left], heap[now]
                            pos[heap[now][1]] = now
                            now = left
                        else:
                            heap[now], heap[right] = heap[right], heap[now]
                            pos[heap[now][1]] = now
                            now = right
                    else:
                        heap[now], heap[left] = heap[left], heap[now]
                        pos[heap[now][1]] = now
                        now = left
                elif right_flag:
                    heap[now], heap[right] = heap[right], heap[now]
                    pos[heap[now][1]] = now
                    now = right
                else:
                    pos[heap[now][1]] = now
                    break

            #更新当前最矮建筑左侧建筑的理论最大高度
            if p > 1 and limit[prev[p]] is None:
                heap_pos = pos[prev[p]]
                delta = p - heap[heap_pos][1]
                if heap[heap_pos][0] > delta + h: 
                    #若成功更新，那么左侧建筑的理论最大高度是变小的，此时需要更新其在堆中的位置
                    heap[heap_pos][0] = delta + h
                    now = heap_pos
                    while now > 0:
                        fa = (now - 1) / 2
                        if heap[now][0] < heap[fa][0]:
                            heap[now], heap[fa] = heap[fa], heap[now]
                            pos[heap[now][1]] = now
                            now = fa
                        else:
                            break
                    pos[heap[now][1]] = now
            
            #更新当前最矮建筑右侧建筑的理论最大高度
            if p <= n and limit[next[p]] is None:
                heap_pos = pos[next[p]]
                delta = heap[heap_pos][1] - p
                if heap[heap_pos][0] > delta + h:
                    heap[heap_pos][0] = delta + h
                    now = heap_pos
                    while now > 0:
                        fa = (now - 1) / 2
                        if heap[now][0] < heap[fa][0]:
                            heap[now], heap[fa] = heap[fa], heap[now]
                            pos[heap[now][1]] = now
                            now = fa
                        else:
                            break
                    pos[heap[now][1]] = now
        
        limit[heap[0][1]] = heap[0][0]

        now_p = 1
        now_h = 0
        res = 0
        while now_p != n:
            next_p = next[now_p]
            next_h = limit[next_p]
            if next_p == n + 1: #对于假定右边界n + 1的特殊处理
                next_p -= 1
                next_h -= 1
            res = max(res, (next_p - now_p - 1 - (abs(next_h - now_h) - 1)) / 2 + max(now_h, next_h))
            now_p, now_h = next_p, next_h
        
        return res
```
