---
title: "683. K个关闭的灯泡"
aliases: ["yiduobo的每日leetcode 683.K个关闭的灯泡"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/604070601"
zhihu_id: "604070601"
zhihu_title: "yiduobo的每日leetcode 683.K个关闭的灯泡"
question_id: "683"
question: "K个关闭的灯泡"
problem_url: "https://leetcode.cn/problems/k-empty-slots/"
created: "2023-02-07T02:08:48+08:00"
updated: "2023-02-07T02:08:48+08:00"
upvotes: 0
comments: 0
---

# 683. K个关闭的灯泡

> **[yiduobo的每日leetcode 683.K个关闭的灯泡](https://zhuanlan.zhihu.com/p/604070601) · 知乎 · 2023-02-07 · 赞同 0**
> 力扣：[683. K个关闭的灯泡](https://leetcode.cn/problems/k-empty-slots/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

683.K个关闭的灯泡

[力扣](https://leetcode.cn/problems/k-empty-slots/)

题题目给出一个开灯的序列，问最早在什么时候会出现两盏距离为k的灯都亮着，且这两盏灯之间的k盏灯都是灭的。很明显，题目要求的情况必然出现在某盏灯被打开的这一刻，不妨设打开的这一盏灯为b，那么需要检测的就是两种情况：

1、b和其左侧位于b - 1 - k的灯都亮着，且二者之间所有灯都是灭的

2、b和其右侧位于b + 1 + k的灯都亮着，且二者之间所有灯都是灭的

对于上面这两种情况，检测单盏灯的亮灭是很容易的，使用一个集合记录当前亮着的灯即可。而对于检测区间中的所有灯是否都是灭的，则可以将其转化为前缀和问题，即区间(l, r)的灯都灭，等价于区间[0, r - 1]中亮的灯的数量等于区间[0, l]中亮的灯的数量，这是一个动态的前缀和问题，也就是使用树状数组的绝佳时机。

到了这里就得到了一种算法：

将开灯的序列进行一趟遍历，使用一个集合记录当前已经打开的灯的编号，以及树状数组记录前缀中亮着的灯的数量和。

接下来，对于当前遍历到的灯b，通过集合检测其左侧left \= b - 1 - k这个编号的灯是否亮着，且区间[0, left]中亮着的灯的数量是否等于区间[0, b - 1]中亮着的灯的数量，若等于，那么(b, b - 1 - k)就是最早符合条件的灯对。

类似的，通过集合检测其右侧right \= b + 1 + k这个编号的灯是否亮着，且区间[0, b]中亮着的灯的数量是否等于区间[0, right - 1]中亮着的灯的数量，若等于，那么(b, b+ 1 + k)就是最早符合条件的灯对。

若上述两种情况都不成立，那么就使用b来更新集合和树状数组，然后继续向后遍历下一盏打开的灯。若遍历完都没有找到符合条件的灯对，那么就返回-1。

最后附上python代码：

```python
class Solution(object):
    def kEmptySlots(self, bulbs, k):
        """
        :type bulbs: List[int]
        :type k: int
        :rtype: int
        """

        illuminated = set()
        n = len(bulbs)
        f = [0] * (n + 1)

        def add(now):
            while now <= n:
                f[now] += 1
                now += now & -now
        
        def get(now):
            s = 0
            while now > 0:
                s += f[now]
                now -= now & -now
            return s

        for index, b in enumerate(bulbs):
            illuminated.add(b)
            left = b - 1 - k
            if left in illuminated and get(left) == get(b - 1):
                return index + 1
            
            right = b + 1 + k
            if right in illuminated and get(right - 1) == get(b):
                return index + 1

            add(b)

        
        return -1
```
