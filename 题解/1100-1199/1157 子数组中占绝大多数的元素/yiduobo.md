---
title: "1157. 子数组中占绝大多数的元素"
aliases: ["yiduobo的每日leetcode 1157.子数组中占绝大多数的元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/378428212"
zhihu_id: "378428212"
zhihu_title: "yiduobo的每日leetcode 1157.子数组中占绝大多数的元素"
question_id: "1157"
question: "子数组中占绝大多数的元素"
problem_url: "https://leetcode.cn/problems/online-majority-element-in-subarray/"
created: "2021-06-07T00:12:45+08:00"
updated: "2021-06-07T00:12:45+08:00"
upvotes: 0
comments: 0
---

# 1157. 子数组中占绝大多数的元素

> **[yiduobo的每日leetcode 1157.子数组中占绝大多数的元素](https://zhuanlan.zhihu.com/p/378428212) · 知乎 · 2021-06-07 · 赞同 0**
> 力扣：[1157. 子数组中占绝大多数的元素](https://leetcode.cn/problems/online-majority-element-in-subarray/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1157.子数组中占绝大多数的元素

[力扣](https://leetcode-cn.com/problems/online-majority-element-in-subarray/)

题目实际上就是给出一个数组，然后求若干子区间的众数。对于区间类问题，一个自然的想法就是利用前缀数组，即对于询问[l, r, threshold]而言，我们可以分别计算出区间[0, l - 1]中每个数出现的次数，然后计算出区间[0, r]中每个数出现的次数，然后用后者减去前者得到区间[l, r]中每个数出现的次数，再判断其中最多的次数是否大于等于threshold。

以样例来说明，对于[1, 1, 2, 2, 1, 1]，此时询问为[2, 3, 2]，那么对于区间[0, 1]，我们有cnt[1] \= 2, cnt[2] \= 0，对于区间[0, 3]，我们有cnt[1] \= 2, cnt[2] \= 2，二者相减之后可以得到cnt[1] \= 0, cnt[2] \= 2，其中较大的cnt[2]满足threshold，因此答案就是2。

但是这样做依然有问题，无论是时间还是空间复杂度都是平方级别的，因此我们需要想办法将问题再次进行转化。

注意观察上面的朴素做法，需要挨个统计每个数出现的次数并进行减法，在这里有两点可以优化起来：

1、随着区间的扩展，统计值数组中仅有一个数会产生变化，因此可以沿用之前的统计结果，但是在空间上由于数组这种数据结构的局限性导致并不好处理。

2、每次求解的时候需要将所有数的出现次数做减法，那么在这里如果利用线段树的话，则可以在O(logn)的时间复杂度内找到出现次数最多的数。

综合以上两点，我们可以使用一种非常规的线段树来处理这个问题。

首先，根据朴素做法，我们需要统计每个数的出现次数，那么到了线段树这里就是我们先建立一颗区间为[1, 20000]的线段树。这里的线段树节点对应的数值，而非区间。对于每一轮来的数值num，我们按线段树更新的方式从根节点向下寻找num对应的节点，同时将路径上的节点值v加上1。这样一来，线段树中每个节点的值就表示了当前子树代表的数值区间中有多少个数。同时由于之前提到的统计数组中仅有一个数会产生变化，那么我们每次更新时就只新建从根节点到num的路径上的节点，而节点原始的左右子树关系则维持不变。换言之，每一轮最多新增O(logn)个节点。为了之后查询，我们在每一轮新增节点时都要将当前最新的根节点保存起来，那么一共会有n个根节点。可以发现，这里的n个根节点实际上就是由于[0, 0]，[0, 1]，[0, 2]，...，[0, n - 1]这n个前缀区间所做成的n棵线段树。

接下来，对于询问[l, r, threshold]，我们就可以找到第l - 1棵以及第r棵前缀线段树，然后从根节点开始向下寻找。

设当前对应的线段树节点为pre和now，而对应的数值区间为[mi, ma]，那么首先可以计算出mid\=(mi + ma) / 2，mid为线段树用来分割区间的中间点。

接下来我们可以先考察now.left.v - pre.left.v是否大于等于threshold。若大于，说明在下标区间[l, r]中有超过threshold个数是落在数值区间[mi, mid]之间的。这也就表明如果存在区间众数，那么其必然位于数值区间[mi, mid]之间，因此我们可以继续向下寻找数值区间[mi, mid]，而此时的线段树节点则应该变为pre.left以及now.left。同样地，若左边不满足但右边满足，我们就应该向下寻找数值区间[mid + 1, ma]，此时对应的线段树节点则为pre.right以及now.right。

重复此过程直到某一时刻mi \= ma或者左右两侧的差都小于threshold为止。对于前面这种情况，说明此时已经找到了具体的数，将其返回即可。而对于后面这种情况，则说明不存在区间众数，返回-1即可。

最后附上python代码：

```python
class Node(object):

    def __init__(self, left=None, right=None, v=0):
        self.left = left
        self.right = right
        self.v = v

class MajorityChecker(object):

    def __init__(self, arr):
        """
        :type arr: List[int]
        """
        self.root_list = [Node()]
    
        self.n = max(arr)
        for num in arr:
            new_root = Node(self.root_list[-1].left, self.root_list[-1].right, self.root_list[-1].v)
            new_root.v += 1
            self.insert(1, self.n, self.root_list[-1], new_root, num)
            self.root_list.append(new_root)

    def insert(self, l, r, pre, now, num):
        if l == r:
            return
        mid = (l + r) >> 1
        if num <= mid:
            if pre and pre.left:
                new_left = Node(pre.left.left, pre.left.right, pre.left.v)
            else:
                new_left = Node()

            new_left.v += 1
            now.left = new_left

            if pre:
                self.insert(l, mid, pre.left, new_left, num)
            else:
                self.insert(l, mid, None, new_left, num)
        
        else:
            if pre and pre.right:
                new_right = Node(pre.right.left, pre.right.right, pre.right.v)
            else:
                new_right = Node()

            new_right.v += 1
            now.right = new_right

            if pre:
                self.insert(mid + 1, r, pre.right, new_right, num)
            else:
                self.insert(mid + 1, r, None, new_right, num)

    def find(self, l, r, pre, now, threshold):
        if l == r:
            return l
        
        mid = (l + r) >> 1

        pre_l = pre_r = 0
        if pre and pre.left:
            pre_l = pre.left.v
        if pre and pre.right:
            pre_r = pre.right.v
        
        if now and now.left and now.left.v - pre_l >= threshold:
            if pre is None:
                return self.find(l, mid, None, now.left, threshold)
            else:
                return self.find(l, mid, pre.left, now.left, threshold)
        
        if now and now.right and now.right.v - pre_r >= threshold:
            if pre is None:
                return self.find(mid + 1, r, None, now.right, threshold)
            else:
                return self.find(mid + 1, r, pre.right, now.right, threshold)
        
        return -1
        
        

    def query(self, left, right, threshold):
        """
        :type left: int
        :type right: int
        :type threshold: int
        :rtype: int
        """

        return self.find(1, self.n, self.root_list[left], self.root_list[right + 1], threshold)

# Your MajorityChecker object will be instantiated and called as such:
# obj = MajorityChecker(arr)
# param_1 = obj.query(left,right,threshold)
```
