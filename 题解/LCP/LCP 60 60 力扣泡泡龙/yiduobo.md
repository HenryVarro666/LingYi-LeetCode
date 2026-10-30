---
title: "LCP 60. 力扣泡泡龙"
aliases: ["yiduobo的每日leetcode LCP60.力扣泡泡龙"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/578859197"
zhihu_id: "578859197"
zhihu_title: "yiduobo的每日leetcode LCP60.力扣泡泡龙"
question_id: "LCP 60"
question: "力扣泡泡龙"
created: "2022-10-31T06:39:24+08:00"
updated: "2022-10-31T06:39:24+08:00"
upvotes: 0
comments: 0
---

# LCP 60. 力扣泡泡龙

> **[yiduobo的每日leetcode LCP60.力扣泡泡龙](https://zhuanlan.zhihu.com/p/578859197) · 知乎 · 2022-10-31 · 赞同 0**
> 力扣：LCP 60. 力扣泡泡龙

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP60.力扣泡泡龙

[力扣](https://leetcode.cn/problems/WInSav/)

没有什么特别好的思路，或者说特别好的算法，比如树分治我现在已经不会写了，那么只能想办法对暴力算法做一些优化。

首先，对于不修改的情况，只需从根节点向下做一次层序遍历就行了。在这里需要统计每一层的节点之和，以及每一层节点的数量。在这里统计节点数量的理由是因为树中节点值可能为负，那么如果后续某次操作删掉了树中整整一行，使得这一行的最终结果变成了一个不存在的0，这也是不合法的，因此可以通过判断删除节点的数量以及该层节点的总数来规避这种情况。

接下来考虑删除节点。一个自然的想法是对于节点now，先优先处理删除now.left以及now.right时，对子树中每一层的层和的影响，并更新删除后最优的层和。接下来，将二者叠加起来就可以得到删除now时对子树中每一层的层和的影响了。

很明显，在最坏情况下这是一个O(n^2)的算法，那么接下来就是想办法优化这个暴力算法了。

首先是对层和的影响。记delta[now][level]为删除now之后对level这一层层和的影响，那么在这里递归求解和可以得到delta[now.left]以及delta[now.right]。接下来需要将这二者合并。在这里可以直接使用浅拷贝，原封不动地将影响层数较多的那一侧的delta据为now所有，然后再使用影响层数较少的那一侧的哈希表来更新delta[now]。

另一方面，如果删除now只对左子树或右子树中的某一侧产生了影响，那么就无须计算删除now之后该层层和的变化，因为这种情况以及在递归求解now的左孩子或者右孩子时计算过了。因此在这里可以再维护一个哈希表need_refresh，其中need_refresh[now]表示删除now之后有哪些层需要计算层和。

同样的，这里的need_refresh也是采用与delta相同的方式进行更新。

除此之外，need_refresh还有一个作用就是由于题目不允许删除拥有两个孩子的节点，那么如果想删除这个节点，就需要将其记录下来，等到回溯到上面某个只有单个孩子的节点时再进行删除，此时就可以将这一层加入到need_refresh中。

最后，由于上面提到的不能删除整一层的节点，因此还需要维护一个remove_size，其中remove_size[now][level]表示的是在删除now之后，level这一层会被删去的节点数目。若某一层level的节点数等于这个remove_size[now][level]，那么就无须计算删除now之后level以一层的层和了。

与上面两个哈希表相同，这里的remove_size同样是通过先挪用大的，然后遍历小的这种方式进行更新。

一般来说，采用上面对哈希表的这种更新方式最终的时间复杂度为O(nlogn)，在这里应该是勉强够用了。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution(object):
    def getMaxLayerSum(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """

        level_sum = []
        level_size = []

        q = [root]
        head = 0
        tail = 1
        while head < tail:
            level_sum.append(0)
            level_size.append(tail - head)
            for now in q[head : tail]:
                level_sum[-1] += now.val
                if now.left:
                    q.append(now.left)
                if now.right:
                    q.append(now.right)
            
            head, tail = tail, len(q)
        
        global res
        res = max(level_sum)
        
        delta = {}
        need_refresh = {}
        remove_size = {}

        def dfs(now, level):
            global res
            if now.left is None:
                if now.right is None:
                    remove_size[now] = {level: 1}
                    need_refresh[now] = set()
                    if level_size[level] == 1:
                        delta[now] = {}
                    else:
                        delta[now] = {level: -now.val}
                        res = max(res, level_sum[level] + delta[now][level])
                else:
                    dfs(now.right, level + 1)
                    delta[now] = delta[now.right]
                    delta[now][level] = now.right.val - now.val
                    remove_size[now] = remove_size[now.right]
                    remove_size[now][level] = 1
                    need_refresh[now] = need_refresh[now.right]
                    need_refresh[now].add(level)

                    for lv in need_refresh[now]:
                        if remove_size[now][lv] < level_size[lv]:
                            res = max(res, level_sum[lv] + delta[now][lv])
                    need_refresh[now] = set()

            elif now.right is None:
                dfs(now.left, level + 1)
                delta[now] = delta[now.left]
                delta[now][level] = now.left.val - now.val
                remove_size[now] = remove_size[now.left]
                remove_size[now][level] = 1
                need_refresh[now] = need_refresh[now.left]
                need_refresh[now].add(level)

                for lv in need_refresh[now]:
                    if remove_size[now][lv] < level_size[lv]:
                        res = max(res, level_sum[lv] + delta[now][lv])
                need_refresh[now] = set()
            
            else:
                dfs(now.left, level + 1)
                dfs(now.right, level + 1)
                
                if len(need_refresh[now.left]) > len(need_refresh[now.right]):
                    refresh_min, refresh_max = need_refresh[now.right], need_refresh[now.left]
                else:
                    refresh_min, refresh_max = need_refresh[now.left], need_refresh[now.right]
                
                need_refresh[now] = refresh_max
                for lv in refresh_min:
                    need_refresh[now].add(lv)
                need_refresh[now].add(level)

                if len(delta[now.left]) > len(delta[now.right]):
                    delta_min, delta_max = delta[now.right], delta[now.left]
                else:
                    delta_min, delta_max = delta[now.left], delta[now.right]
                
                delta[now] = delta_max
                for lv in delta_min:
                    delta[now][lv] = delta[now].get(lv, 0) + delta_min[lv]
                    need_refresh[now].add(lv)
                delta[now][level] = now.left.val + now.right.val - now.val
                

                if len(remove_size[now.left]) > len(remove_size[now.right]):
                    remove_min, remove_max = remove_size[now.right], remove_size[now.left]
                else:
                    remove_min, remove_max = remove_size[now.left], remove_size[now.right]
                
                remove_size[now] = remove_max
                for lv in remove_min:
                    remove_size[now][lv] += remove_min[lv]
                remove_size[now][level] = 1

        dfs(root, 0)
        return res
```
