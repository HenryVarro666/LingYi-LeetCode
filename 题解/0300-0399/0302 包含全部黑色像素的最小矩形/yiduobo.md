---
title: "302. 包含全部黑色像素的最小矩形"
aliases: ["yiduobo的每日leetcode 302.包含全部黑色像素的最小矩形"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/595580496"
zhihu_id: "595580496"
zhihu_title: "yiduobo的每日leetcode 302.包含全部黑色像素的最小矩形"
question_id: "302"
question: "包含全部黑色像素的最小矩形"
problem_url: "https://leetcode.cn/problems/smallest-rectangle-enclosing-black-pixels/"
created: "2022-12-30T21:53:35+08:00"
updated: "2022-12-30T21:53:35+08:00"
upvotes: 0
comments: 0
---

# 302. 包含全部黑色像素的最小矩形

> **[yiduobo的每日leetcode 302.包含全部黑色像素的最小矩形](https://zhuanlan.zhihu.com/p/595580496) · 知乎 · 2022-12-30 · 赞同 0**
> 力扣：[302. 包含全部黑色像素的最小矩形](https://leetcode.cn/problems/smallest-rectangle-enclosing-black-pixels/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

302.包含全部黑色像素的最小矩形

[力扣](https://leetcode.cn/problems/smallest-rectangle-enclosing-black-pixels/)

注意到题目保证了图中只有一块连通的黑色像素，那么包含这块黑色像素的最小矩形就取决与这块黑色像素在上下左右四个方向最远的坐标是多少，而对于这些坐标的求解则可以利用二分法。

以求解最上侧的坐标为例。由于一开始已经知道(x, y)是黑色块，那么最上侧坐标二分的上下边界就分别是0和x。接下来对于二分到的mid，则可以通过枚举mid这一行，看看其中是否有黑色块。若有，那么就可以调整二分的上界为mid，否则需要调整二分的下界为mid + 1。

这样一来，就可以在O(nlogm)的时间内找出最上侧的坐标。

而对于另外三个坐标则可以如法炮制，那么最终就可以在O(mlogn + nlogm)的时间内找出所有的四个坐标，从而计算出最终答案了。

需要注意二分法在具体实现时，需要注意上下边界需要根据具体情况来进行调整。

最后附上python代码：

```python
class Solution(object):
    def minArea(self, image, x, y):
        """
        :type image: List[List[str]]
        :type x: int
        :type y: int
        :rtype: int
        """

        m = len(image)
        n = len(image[0])

        def check_h(i):
            for j in range(n):
                if image[i][j] == '1':
                    return True

            return False

        def check_v(j):
            for i in range(m):
                if image[i][j] == '1':
                    return True
            
            return False

        def binary_search(head, tail, delta, check):
            while head < tail:
                mid = (head + tail + delta) >> 1
                if check(mid):
                    if delta == 0:
                        tail = mid
                    else:
                        head = mid
                else:
                    if delta == 0:
                        head = mid + 1
                    else:
                        tail = mid - 1

            return head

        top = binary_search(0, x, 0, check_h)
        bottom = binary_search(x, m - 1, 1, check_h)
        left = binary_search(0, y, 0, check_v)
        right = binary_search(y, n - 1, 1, check_v)

        return (bottom - top + 1) * (right - left + 1)
```
