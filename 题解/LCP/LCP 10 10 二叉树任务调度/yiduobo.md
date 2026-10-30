---
title: "LCP 10. 二叉树任务调度"
aliases: ["yiduobo的每日leetcode LCP10.二叉树任务调度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/570888612"
zhihu_id: "570888612"
zhihu_title: "yiduobo的每日leetcode LCP10.二叉树任务调度"
question_id: "LCP 10"
question: "二叉树任务调度"
problem_url: "https://leetcode.cn/problems/er-cha-shu-ren-wu-diao-du/"
created: "2022-10-06T04:08:29+08:00"
updated: "2022-10-06T04:08:29+08:00"
upvotes: 0
comments: 0
---

# LCP 10. 二叉树任务调度

> **[yiduobo的每日leetcode LCP10.二叉树任务调度](https://zhuanlan.zhihu.com/p/570888612) · 知乎 · 2022-10-06 · 赞同 0**
> 力扣：[LCP 10. 二叉树任务调度](https://leetcode.cn/problems/er-cha-shu-ren-wu-diao-du/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP10.二叉树任务调度

[力扣](https://leetcode.cn/problems/er-cha-shu-ren-wu-diao-du/)

由于树中所有任务所需的时间总和为常数，且root自身的任务只能串行，那么为了使得总的执行时间最短，就应该尽量让左右两颗子树中的任务并行起来。

不妨设在尽量并行的情况下，执行完左子树中所有任务所需的串行时间为left_s_time，并行时间为left_p_time，执行完右子树中所有任务所需的串行时间为right_s_time，并行时间为right_p_time。

最直观的想法自然是先让left_s_time和right_s_time中的任务并行起来。在最好的情况下，left_s_time刚好等于right_s_time，此时树中除root自身任务外的所有任务都是并行的，最终的串行时间就是root.val，并行时间则是left_p_time + right_p_time + left_s_time，即左右子树原本的并行时间，加上左右子树原有串行任务转并行后需要的时间。

当left_s_time不等于right_s_time时，就需要另想办法调度了。题目非常好心地给出了样例3，在样例3中，左子树的串行时间为3，右子树的串行时间为2，并行时间为4。在完成最基本的串行时间配对后，左子树还剩余1单位时间的串行任务，在这里可以采用轮流让右子树中的并行任务与左子树中这个1单位的时间的串行任务配对并行，即将这个1拆分成两个0.5，而右子树中的两个4分别拆分出0.5与之配对，然后右子树中剩余的两个3.5再按原计划配对执行。这样一来，就相当于将左子树这个1单位时间的任务给并行化了。

根据这个配对规则，可以发现在这种情况下，右子树中的两个4最多可以供应左子树中8的串行任务进行配对。

更一般的，当left_s_time > right_s_time时，记delta \= left_s_time - right_s_time，那么当delta \<\= right_p_time \* 2时，就可以通过上面的配对方法让所有任务并行起来，此时整棵树的串行时间就是root自身任务所需的时间root.val，而并行时间则为left_p_time + right_p_time + right_s_time + delta / 2。而当delta > right_p_time \* 2时，多出的delta - right_p_time \* 2的这些任务也只能串行，那么整棵树的串行时间就是root.val + delta - right_p_time \* 2，而并行时间则为left_p_time + right_p_time + right_s_time + right_p_time。

反之，当left_s_time \< right_s_time时，将上面结论中的left和right互换就行了。

到了这里，就只需从root开始，先递归求解root.left和root.right，得到左右子树各自的串行和并行时间，然后根据上面的结论为左右子树的串行时间进行配对，从而得到整棵树自身的串行和并行时间。二者相加即为最终答案。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def minimalExecTime(self, root):
        """
        :type root: TreeNode
        :rtype: float
        """

        def dfs(now):
            if not now.left:
                if not now.right:
                    return now.val, 0
                else:
                    s_time, p_time = dfs(now.right)
                    return s_time + now.val, p_time
            elif not now.right:
                s_time, p_time = dfs(now.left)
                return s_time + now.val, p_time
            else:
                left_s_time, left_p_time = dfs(now.left)
                right_s_time, right_p_time = dfs(now.right)
                if left_s_time == right_s_time:
                    return now.val, left_s_time + left_p_time + right_p_time
                elif left_s_time > right_s_time:
                    delta = left_s_time - right_s_time
                    if delta <= right_p_time + right_p_time:
                        return now.val, right_s_time + delta * 0.5 + left_p_time + right_p_time
                    else:
                        return now.val + delta - right_p_time - right_p_time, right_s_time + right_p_time + left_p_time + right_p_time
                else:
                    delta = right_s_time - left_s_time
                    if delta <= left_p_time + left_p_time:
                        return now.val, left_s_time + delta * 0.5 + left_p_time + right_p_time
                    else:
                        return now.val + delta - left_p_time - left_p_time, left_s_time + left_p_time + left_p_time + right_p_time
        
        s_time, p_time = dfs(root)
        return s_time + p_time
```
