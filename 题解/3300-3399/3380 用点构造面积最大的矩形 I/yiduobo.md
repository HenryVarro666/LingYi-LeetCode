---
title: "3380. 用点构造面积最大的矩形I & 3382. 用点构造面积最大的矩形II"
aliases: ["yiduobo的每日leetcode 3380.用点构造面积最大的矩形I && 3382.用点构造面积最大的矩形II", "3380. 用点构造面积最大的矩形I", "3382. 用点构造面积最大的矩形II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-indexed-tree", "leetcode/hash-table", "leetcode/binary-search", "leetcode/hard", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树", "题单/常用数据结构/专题-离线算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/29317687362"
zhihu_id: "29317687362"
zhihu_title: "yiduobo的每日leetcode 3380.用点构造面积最大的矩形I && 3382.用点构造面积最大的矩形II"
question_id: ["3380", "3382"]
question: ["用点构造面积最大的矩形 I", "用点构造面积最大的矩形 II"]
problem_url: ["https://leetcode.cn/problems/maximum-area-rectangle-with-point-constraints-i/", "https://leetcode.cn/problems/maximum-area-rectangle-with-point-constraints-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2723
created: "2025-03-11T01:38:38+08:00"
updated: "2025-03-11T01:38:38+08:00"
upvotes: 1
comments: 0
---

# 3380. 用点构造面积最大的矩形I & 3382. 用点构造面积最大的矩形II

> **[yiduobo的每日leetcode 3380.用点构造面积最大的矩形I && 3382.用点构造面积最大的矩形II](https://zhuanlan.zhihu.com/p/29317687362) · 知乎 · 2025-03-11 · 赞同 1**
> 力扣：[3380. 用点构造面积最大的矩形 I](https://leetcode.cn/problems/maximum-area-rectangle-with-point-constraints-i/) · Medium · 灵茶山艾府：[非暴力做法：离线询问+离散化+树状数组（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3382. 用点构造面积最大的矩形 II](https://leetcode.cn/problems/maximum-area-rectangle-with-point-constraints-ii/) · Hard · 灵茶山艾府：[离线询问+离散化+树状数组（Python/Java/C++/Go）](../3382%20用点构造面积最大的矩形%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3380.用点构造面积最大的矩形I

[3380. 用点构造面积最大的矩形 I - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-area-rectangle-with-point-constraints-i/description/)

3382.用点构造面积最大的矩形II

[3382. 用点构造面积最大的矩形 II - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-area-rectangle-with-point-constraints-ii/)

题目给出平面上的一些整数坐标点，这些点互不相同。要求从这些点中找出四个点，满足：

1、这四个点恰好是某个矩形的四个顶点，且这个矩形与坐标轴平行

2、矩形内部不能包含其他的点

问可以得到的最大矩形面积是多少。如果无法构造，那么返回-1。

两题的题设相同，第二题的数据规模较大，点的规模可以达到2 \* 10^5，而坐标值则可以达到8 \* 10^7。

---

根据题目中对于矩形的要求，若矩形的左下角为(x1, y1)，那么：

1、左上角的点(x1, y2)只能是x1这一列上刚好位于(x1, y1)上面的那个点，理由是不能有其他点被包含在矩形内，因此(x1, y1)到(x1, y2)之间不能存在其他的点

2、右下角的点(x2, y1)只能是y1这一行上刚好位于(x1, y1)右侧的那个点，理由与上面类似

根据以上两点，就可以先通过对这些点按x和y分别排序，就可以通过哈希表记录每个点上面最近的点以及右侧最近的点是哪个点。接下来枚举每个点作为矩形的左下角，根据哈希表就可以得到左上角以及右下角的点的坐标，从而推导出右上角点的坐标。若右上角的点存在，那么只需判断矩形内部是否存在其他的点，若不存在，就可以使用当前矩形的面积更新答案了。

---

明确了枚举点的方法，接下来的问题就是如何计算矩形内部点的数目。

对于这个问题，首先可以利用二维前缀和将问题从矩形内部有多少个点，转化为以(0, 0)为左下角，(x, y)为右上角的矩形内有多少个点，计这个值为cnt[(x, y)]。那么对于以(x1, y1)为左下角，(x2, y2)为右上角中内点的数目，就可以通过类似二维前缀和的方法，使用cnt[(x2, y2)] - cnt[(x1, y2)] - cnt[(x2, y1)] + cnt[(x1, y1)] + 3得到，这里加3的含义是这个式子会将(x1, y2)、(x2, y1)、(x1, y1)去除掉，所以需要加回来。

而对于本题，如果要求(x1, y1)为左下角，(x2, y2)为右上角的矩形中没有其他的点，那么就要使得上面的式子等于4，化简后就是cnt[(x2, y2)] - cnt[(x1, y2)] - cnt[(x2, y1)] + cnt[(x1, y1)] \= 1。

---

接下来的问题就是如何计算cnt[(x, y)]。可以发现，cnt[(x, y)]实际上就有所有点中有多少个点的横坐标小于等于x且纵坐标小于等于y。对于这个问题，在坐标数值较小时可以利用二维树状数组求解，而对于本题，使用分治法是比较合适的。对于这类多个维度比大小的问题，一种常见的思路是先按某个维度排序，然后再对另一个维度执行归并排序，在排序过程中就可以在保证序的前提下统计数目。

具体来说，先对x从小到大进行排序，接下来对y进行归并排序。对于当前执行归并排序的部分[left, right]：

1、若left等于right：

此时只有一个元素，无需排序也无需统计，直接返回即可

2、若left \< right：

令mid \= (left + right) // 2，先递归求解[left, mid]以及[mid + 1, right]。

递归求解完成后，此时[left, mid]以及[mid + 1, right]中的点都是按y排好序的，且[left, mid]中的点的x都小于等于[mid + 1, right]中的点的x。

接下来对[left, mid]和[mid + 1, right]执行二路归并。对于当前比较的左半边的i以及右半边的j：

2-1）若当前的i到达mid + 1，或者当前i的y大于j的y：

说明[left, i - 1]这一段的y都小于等于j的y，而[i, mid]这一段的y则都大于y，因此在[left, mid]这一段中，有i - left个点的需要被累加到cnt中。除此之外，还需要将节点j加入到排序结果数组中，然后将j向后移动

2-2）否则：

此时只需将节点i加入到排序结果数组中，然后将i向后移动

---

到了这里，就得到的完整的算法：

1、首先将节点按x排序，然后对y执行归并排序，在排序过程中计算每个节点对应的cnt[(x, y)]

2、然后再将节点按x为第一关键字，y为第二关键字排序。接下来遍历每个节点，若相邻节点间的x坐标相同，说明后一个节点恰好就是前一个节点在同一列的上一个节点，使用一个哈希表up就每个节点在同一列中的上一个节点坐标

3、最后将节点按y为第一关键字，x为第二关键字排序。接下来遍历每个节点(x1, y1)：

若up[(x1, y1)]存在，那么就从中获取对应的y2，否则跳过当前节点。

另一方面，若下一个节点的y与y1相同，那么下一个节点的x就是x2，否则跳过当前节点。

得到x2和y2后，若(x2, y2)存在，且cnt[(x2, y2)] - cnt[(x1, y2)] - cnt[(x2, y1)] + cnt[(x1, y1)] \= 1，那么就是用矩形的面积，即(x2 - x1) \* (y2 - y1)更新答案。

最后附上3382题的python代码，3380题的输入是直接给出points：

```python
class Solution(object):
    def maxRectangleArea(self, xCoord, yCoord):
        """
        :type xCoord: List[int]
        :type yCoord: List[int]
        :rtype: int
        """
        
        points = zip(xCoord, yCoord)

        cnt = {}
        points.sort()
        for x, y in points:
            cnt[(x, y)] = 1
        
        def calc(points, left, right):
            if left == right:
                return
            
            mid = (left + right) >> 1
            calc(points, left, mid)
            calc(points, mid + 1, right)
            
            i = left
            j = mid + 1
            tmp = []
            while i <= mid or j <= right:
                if i == mid + 1 or (j <= right and points[i][1] > points[j][1]):
                    cnt[(points[j][0], points[j][1])] += i - left
                    tmp.append(points[j][:])
                    j += 1
                else:
                    tmp.append(points[i][:])
                    i += 1

            for index, (x, y) in enumerate(tmp):
                points[index + left] = [x, y]

        calc(points, 0, len(points) - 1)
        
        points.sort()
        up = {}
        for index in range(len(points) - 1):
            if points[index][0] == points[index + 1][0]:
                up[(points[index][0], points[index][1])] = points[index + 1][:]
        
        points.sort(key=lambda d:(d[1], d[0]))
        res = -1
        for index in range(len(points) - 1):
            x1, y1 = points[index]
            if (x1, y1) not in up:
                continue
            if points[index + 1][1] != points[index][1]:
                continue
            x2, y2 = points[index + 1][0], up[(x1, y1)][1]
            if (x2, y2) in cnt and cnt[(x2, y2)] - cnt[(x1, y2)] - cnt[(x2, y1)] + cnt[(x1, y1)] == 1:
                res = max(res, (x2 - x1) * (y2 - y1))
        
        return res
```
