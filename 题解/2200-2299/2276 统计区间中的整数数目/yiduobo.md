---
title: "2276. 统计区间中的整数数目"
aliases: ["yiduobo的每日leetcode 2276.统计区间中的整数数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "leetcode/ping-heng-shu", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/550748868"
zhihu_id: "550748868"
zhihu_title: "yiduobo的每日leetcode 2276.统计区间中的整数数目"
question_id: "2276"
question: "统计区间中的整数数目"
problem_url: "https://leetcode.cn/problems/count-integers-in-intervals/"
difficulty: "Hard"
rating: 2222
created: "2022-08-07T01:38:58+08:00"
updated: "2022-08-07T01:38:58+08:00"
upvotes: 1
comments: 2
---

# 2276. 统计区间中的整数数目

> **[yiduobo的每日leetcode 2276.统计区间中的整数数目](https://zhuanlan.zhihu.com/p/550748868) · 知乎 · 2022-08-07 · 赞同 1**
> 力扣：[2276. 统计区间中的整数数目](https://leetcode.cn/problems/count-integers-in-intervals/) · Hard · 灵茶山艾府：[两种做法：珂朵莉树 / 动态开点线段树（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2276.统计区间中的整数数目

[力扣](https://leetcode.cn/problems/count-integers-in-intervals/)

经典的动态区间合并问题。本题的数据规模以及区间边界都非常大，同时本题还是个在线问题，这也就意味着无法使用排序后离散化映射将区间边界从1到10^9缩减到1到10^5，这也就意味着树状数组以及常规的线段树都是不能用的。

到了这里，能用的似乎就只有平衡二叉树和动态新建节点的线段树了。

我在这里采用的是线段树。与常规的线段树不同，一开始建树时并不会将树中所有节点建好，而是只构造一个根节点，管辖范围为1到10^9。接下来对于插入的区间，根据当前节点管辖范围与区间的包含关系判断应该递归求解哪些区间。若要求解的区间对应的节点不存在，那么就新建这个节点。这样一来，就可以保证树的节点规模不超过4 \* 10^5，保证了空间复杂度不会过高。

由于本题的询问是区间内被覆盖节点的数目，那么在常规的树结构外还需要额外新增一个遍历cnt，用来储存当前节点管辖的区间内已经被覆盖住的节点数目。在每一次更新过后，当前节点的cnt自然是等于左孩子的cnt与右孩子的cnt之和。

另外在具体实现上还有两个优化点。第一个是对于某一次更新，若当前节点管辖的区间已经全部被覆盖住了，也就是该节点的cnt等于该节点管辖的区间长度，那么就无须再对本次更新进行任何操作。第二个则是若某次更新时，更新的覆盖区间恰好与节点管辖的区间重叠，那么只需要更新当前节点的覆盖状态，即更新当前节点的cnt为当前节点的区间长度，而不需要继续向下递归更新。

最后附上python代码：

```python
class CountIntervals(object):

    def __init__(self):
        self.node_list = [[1, 10 ** 9, -1, -1, 0]]

    def update(self, now, left, right):
        l, r, left_child, right_child, cnt = self.node_list[now]

        if r - l + 1 == cnt:
            return
        
        if l == left and r == right:
            self.node_list[now][-1] = right - left + 1
            return
        
        mid = (l + r) >> 1
        if right <= mid:
            if left_child == -1:
                self.node_list.append([l, mid, -1, -1, 0])
                left_child = self.node_list[now][2] = len(self.node_list) - 1
            self.update(left_child, left, right)
        
        elif left > mid:
            if right_child == -1:
                self.node_list.append([mid + 1, r, -1, -1, 0])
                right_child = self.node_list[now][3] = len(self.node_list) - 1
            self.update(right_child, left, right)
        
        else:
            if left_child == -1:
                self.node_list.append([l, mid, -1, -1, 0])
                left_child = self.node_list[now][2] = len(self.node_list) - 1
            self.update(left_child, left, mid)

            if right_child == -1:
                self.node_list.append([mid + 1, r, -1, -1, 0])
                right_child = self.node_list[now][3] = len(self.node_list) - 1
            self.update(right_child, mid + 1, right)

        self.node_list[now][-1] = 0

        if left_child > 0:
            self.node_list[now][-1] += self.node_list[left_child][-1]
        
        if right_child > 0:
            self.node_list[now][-1] += self.node_list[right_child][-1]
            
    def add(self, left, right):
        """
        :type left: int
        :type right: int
        :rtype: None
        """
        self.update(0, left, right)

    def count(self):
        """
        :rtype: int
        """

        return self.node_list[0][-1]

# Your CountIntervals object will be instantiated and called as such:
# obj = CountIntervals()
# obj.add(left,right)
# param_2 = obj.count()
```
