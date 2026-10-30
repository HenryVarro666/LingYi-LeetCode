---
title: "850. 矩形面积II"
aliases: ["yiduobo的每日leetcode 850.矩形面积II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "leetcode/sorting", "leetcode/sweep-line", "题单/常用数据结构", "题单/常用数据结构/二-差分", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/348397810"
zhihu_id: "348397810"
zhihu_title: "yiduobo的每日leetcode 850.矩形面积II"
question_id: "850"
question: "矩形面积 II"
problem_url: "https://leetcode.cn/problems/rectangle-area-ii/"
difficulty: "Hard"
rating: 2236
created: "2021-02-01T22:25:38+08:00"
updated: "2021-02-01T22:25:38+08:00"
upvotes: 0
comments: 1
---

# 850. 矩形面积II

> **[yiduobo的每日leetcode 850.矩形面积II](https://zhuanlan.zhihu.com/p/348397810) · 知乎 · 2021-02-01 · 赞同 0**
> 力扣：[850. 矩形面积 II](https://leetcode.cn/problems/rectangle-area-ii/) · Hard · 灵茶山艾府：[Lazy 线段树 + 扫描线（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

850.矩形面积II

[力扣](https://leetcode-cn.com/problems/rectangle-area-ii/)

最直观的做法自然是利用容斥原理，不过这样就需要枚举所有的矩形组合，时间复杂度太高，需要另想办法。

仔细观察样例的图，我们除了按题目描述将问题视作若干矩形重叠，也可以按照x轴进行分段。例如样例中，对于x轴上0到1的部分，其提供了面积2；对于x轴上1到2的部分，其提供了面积3；最后对于x轴上2到3的部分，其提供了面积1。因此，最终的面积为6。

分析输入的矩形以及按x轴划分的面积可以发现，在x轴上的区间划分就是矩形输入的横坐标排序按顺序进行划分，而每一段的面积则取决于所有矩形在当前x轴区间上生效的纵坐标区间之和。还是以样例举例：

在x轴的0到1这一段，只有第一个矩形的0到2生效，因此面积为2

在x轴的1到2这一段，有第一个矩形的0到2生效，有第二个矩形的0到3生效，还有第三个矩形的0到1生效。将这三段合起来，那么最终生效的就是0到3，因此面积为3

在x轴的2到3这一段，只有第三个矩形的0到1生效，因此面积为1

到了这里可以发现，面积的计算实际上是某种动态区间合并的问题。

于是现在就有了一种做法：

1、将所有矩形组织成(x1, y1, y2)，(x2, y1, y2)这两个三元组的形式，然后按照x的大小从小到大进行排序

2、遍历排序后的结果，设当前遍历到的三元组为第i个，那么此时的x轴区间就是delta_x \= x[i] - x[i - 1]

3、计算当前x轴区间内纵坐标覆盖的长度，设为k，那么这里将提供面积k \* delta_x

4、若当前三元组是矩形左侧形成的三元组，那么将y1[i]到y2[i]这一段加入到目前的区间中，否则从目前的区间中去除掉y1[i]到y2[i]这一段。由于我们已经按x进行了排序，那么可以保证每次去除操作执行之前必然已经执行过了加入操作。

但是上面这种做法也存在一个问题，就是区间的跨度太多，进行区间合并的复杂度较高。不过注意到这里的区间合并我们只关心区间的相对大小，因此可以先将输入的所有y收集起来，排序之后按顺序进行映射。由于最多只有200个矩形，因此按y的大小排序最多就是0到399，那么此时就可以将原始的y映射到0到399这样一个较小的区间了。

最后，对于区间合并问题，可以使用线段树提高效率，不过由于这里区间在离散化后跨度仅为0到399，直接使用暴力法也是可以的。

最后附上python代码，其中mapping_dict以及re_mapping_dict分别为y的值到y的顺序的映射以及反映射，f为线段树。

在这里线段树的get操作有一个很便利的地方是，若当前整棵子树被赋值过，说明当前存在一个生效的区间完全包含了当前区间，因此可以直接返回末尾减去头部：

```python
class Solution(object):
    def rectangleArea(self, rectangles):
        """
        :type rectangles: List[List[int]]
        :rtype: int
        """

        line_list = []
        height_list = []
        mapping_dict = {}
        re_mapping_dict = {}
        for x1, y1, x2, y2 in rectangles:
            height_list.append(y1)
            height_list.append(y2)

        cnt = 0
        now = None
        for index, height in enumerate(sorted(height_list)):
            if height != now:
                mapping_dict[height] = cnt
                re_mapping_dict[cnt] = height
                cnt += 1
                now = height
        
        for x1, y1, x2, y2 in rectangles:
            line_list.append([x1, mapping_dict[y1], mapping_dict[y2], 1])
            line_list.append([x2, mapping_dict[y1], mapping_dict[y2], -1])
        
        mod = 10 ** 9 + 7
        line_list = sorted(line_list, key=lambda d:d[0])
        last_x = line_list[0][0]
        f = [0] * 1024
        res = 0
        self.put(0, 0, cnt - 1, line_list[0][1], line_list[0][2] - 1, line_list[0][3], f)
        for x, y1, y2, delta in line_list[1:]:
            if x != last_x:
                res = (res + (x - last_x) * self.get(0, 0, cnt - 1, f, re_mapping_dict)) % mod
                last_x = x
            self.put(0, 0, cnt - 1, y1, y2 - 1, delta, f)

        return res

    def put(self, now, left, right, i, j, delta, f):
        if i > j:
            return
        if left == i and right == j:
            f[now] += delta
        else:
            mid = (left + right) / 2
            if j <= mid:
                self.put(now + now + 1, left, mid, i, j, delta, f)
            elif i > mid:
                self.put(now + now + 2, mid + 1, right, i, j, delta, f)
            else:
                self.put(now + now + 1, left, mid, i, mid, delta, f)
                self.put(now + now + 2, mid + 1, right, mid + 1, j, delta, f)
        
    def get(self, now, left, right, f, re_mapping_dict):
        if left > right:
            return 0
        if f[now] > 0:
            return re_mapping_dict[right + 1] - re_mapping_dict[left]
        elif left == right:
            return 0
        else:
            mid = (left + right) / 2
            return self.get(now + now + 1, left, mid, f, re_mapping_dict) + self.get(now + now + 2, mid + 1, right, f, re_mapping_dict)
```
