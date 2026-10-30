---
title: "1956. 感染K种病毒所需的最短时间"
aliases: ["yiduobo的每日leetcode 1956.感染K种病毒所需的最短时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/624089127"
zhihu_id: "624089127"
zhihu_title: "yiduobo的每日leetcode 1956.感染K种病毒所需的最短时间"
question_id: "1956"
question: "感染K种病毒所需的最短时间"
problem_url: "https://leetcode.cn/problems/minimum-time-for-k-virus-variants-to-spread/"
created: "2023-04-23T04:11:29+08:00"
updated: "2023-04-23T04:11:29+08:00"
upvotes: 0
comments: 0
---

# 1956. 感染K种病毒所需的最短时间

> **[yiduobo的每日leetcode 1956.感染K种病毒所需的最短时间](https://zhuanlan.zhihu.com/p/624089127) · 知乎 · 2023-04-23 · 赞同 0**
> 力扣：[1956. 感染K种病毒所需的最短时间](https://leetcode.cn/problems/minimum-time-for-k-virus-variants-to-spread/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1956.感染K种病毒所需的最短时间

[力扣](https://leetcode.cn/problems/minimum-time-for-k-virus-variants-to-spread/)

对于位于(x, y)的某种病毒，其传播t天之后将会感染一个以(x, y)为中心，对角线长度为2t的正菱形，因此本题实际上问的是给出若干个菱形中点，要求找出最小的t，使得以这些中心构造的对角线长度为2t的正菱形有至少k个菱形都覆盖了同一个整数点。

可以发现，t越大菱形覆盖的面积就越大，因此在这里可以使用二分法来寻找这个最小的t。

对于二分的初始值，下界自然是0，而上界则应该是两个点曼哈顿距离乘以二分之根号2。由于需要是整数，因此这里在上界应该向上取整。

确定上下界的初始值之后开始进行二分，对于当前二分到的mid，需要确定最多有多少个菱形相交。

菱形的相交是不太好处理的，因此在这里需要做一次坐标变换，将坐标轴逆时针旋转45度，这样一来所有的菱形就变成了正方形，问题就变成了给出若干个正方形，问是否存在某个整数点被最少k个正方形覆盖。

由于原点没有变换，坐标变换的计算方法就是：

x' \= x \* cosθ + y \* sinθ \= (x +y) \* sqrt(2) / 2

y' \= y \* cosθ - x \* sinθ \= (y - x) \* sqrt(2) / 2

为了方便计算，在这里还可以将变换后的所有坐标乘以根号2，这样一来就消除了最后这一项sqrt(2) / 2，使得变换完之后的点依然是整数点。

得到变换后的坐标后，问题就变成了经典的给出若干矩形问相交的情况。对于这个问题，效率最高的做法是扫描线配合树状数组进行求解，不过在这里n最大只有50，因此可以使用暴力算法来求解相交的情况。

具体实现上，可以将正方形的左右两条边取出来，按x坐标从小到大进行排序。接下来一趟遍历，使用一个变量x_cnt记录当前的x坐标位于多少个正方形内部，以及两个哈希表记录下边和上边的y坐标出现的次数。每当遇到一条左侧边是，将x_cnt加上1并将上下两个y坐标出现的次数加上1，否则就将x_cnt减去1同时将上下两个y坐标出现的次数减去1。当x_cnt大于等于k或者x_cnt从k变为k - 1时，当前的x坐标就必然位于至少k个正方形内，接下来则需要找出合法的y坐标。

y坐标的处理方法与处理x坐标相同，使用一个数组统计所有的下边和上边的y坐标，从小到大排序后一趟遍历，使用一个变量y_cnt记录当前的y坐标位于多少个正方形内部。每当遇到一条下侧边，将y_cnt加上1，否则就将y_cnt减去1。当y_cnt大于等于k或者y_cnt从k变为k - 1时，当前的y坐标就必然位于至少k个正方形内，那么此时的(x, y)就位于至少k个正方形内。

需要特别注意的是，当前的(x, y)可能并不是整数点，但是经过坐标变换之后变成了整数点，因此需要检测(x, y)在变换回原始坐标之后是否依然被至少k个菱形覆盖。另一方面，由于检测点都位于正方形的边界上，因此可能出现检测点并不是整点，但是其附近存在整点位于正方形内部但不位于正方形边界，于是在检测时可以在坐标变换回去之后适当向外侧检测一圈整数点。

若找出了符合条件的整数点，那么就将二分的上边界调整为mid，否则就将下边界调整为mid + 1。

最后附上python代码：

```python
class Solution(object):
    def minDayskVariants(self, points, k):
        """
        :type points: List[List[int]]
        :type k: int
        :rtype: int
        """

        def check(x, y, mid):
            ori_x = int((x - y) / 2.0)
            ori_y = int((x + y) / 2.0)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    cnt = 0
                    cx = ori_x + dx
                    cy = ori_y + dy
                    for px, py in points:
                        if abs(cx - px) + abs(cy - py) <= mid:
                            cnt += 1
                    
                    if cnt >= k:
                        return True
            
            return False

        max_dis = 0
        n = len(points)
        for i in range(n - 1):
            for j in range(i + 1, n):
                max_dis = max(max_dis, abs(points[i][0] - points[j][0]) + abs(points[j][0] - points[j][1]))
        
        left = 0
        right = int(max_dis * 0.75) + 1
        while left < right:
            mid = (left + right) / 2
            trans_points = []
            for i in range(n):
                x, y = points[i][0], points[i][1]
                up_y, down_y = y + mid, y - mid
                x1, y1 = x + down_y, down_y - x
                x2, y2 = x + up_y, up_y - x
                trans_points.append([x1, y1, y2, 1])
                trans_points.append([x2, y1, y2, -1])
            
            trans_points.sort(key = lambda d:(d[0], -d[-1]))

            x_cnt = 0
            y1_dict = {}
            y2_dict = {}
            flag = False

            for x, y1, y2, delta in trans_points:
                x_cnt += delta
                if delta == 1:
                    y1_dict[y1] = y1_dict.get(y1, 0) + 1
                    y2_dict[y2] = y2_dict.get(y2, 0) + 1
                else:
                    y1_dict[y1] -= 1
                    y2_dict[y2] -= 1
                
                if x_cnt >= k or (x_cnt == k - 1 and delta == -1):
                    y_list = []
                    for y1 in y1_dict:
                        for freq in range(y1_dict[y1]):
                            y_list.append([y1, 1])
                    for y2 in y2_dict:
                        for freq in range(y2_dict[y2]):
                            y_list.append([y2, -1])

                    y_list.sort(key=lambda d:(d[0], -d[-1]))
                    y_cnt = 0
                    for y, delta in y_list:
                        y_cnt += delta
                        if (y_cnt >= k or (y_cnt == k - 1 and delta == -1)) and check(x, y, mid):
                            flag = True
                            break
                    
                    if flag:
                        break
            
            if flag:
                right = mid
            else:
                left = mid + 1
        
        return left
```
