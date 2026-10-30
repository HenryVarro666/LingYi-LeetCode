---
title: "75. 颜色分类"
aliases: ["yiduobo的每日leetcode 75.颜色分类"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/LeetCode-热题-100", "题单/滑动窗口与双指针/三-单序列双指针", "题单/LeetCode-热题-100/技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/133328594"
zhihu_id: "133328594"
zhihu_title: "yiduobo的每日leetcode 75.颜色分类"
question_id: "75"
question: "颜色分类"
problem_url: "https://leetcode.cn/problems/sort-colors/"
difficulty: "Medium"
created: "2020-04-18T23:45:22+08:00"
updated: "2020-04-18T23:45:22+08:00"
upvotes: 0
comments: 0
---

# 75. 颜色分类

> **[yiduobo的每日leetcode 75.颜色分类](https://zhuanlan.zhihu.com/p/133328594) · 知乎 · 2020-04-18 · 赞同 0**
> 力扣：[75. 颜色分类](https://leetcode.cn/problems/sort-colors/) · Medium · 灵茶山艾府：[O(n) 插入排序，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

75.颜色分类<https://leetcode-cn.com/problems/sort-colors/>

很有意思的题目。对于bbb...bbba这种串，要将a放到b的左边，一个简单的思路就是将a与最左侧的那个b进行交换，这样就用O(1)的时间完成了段落的移动。

对于这个题目，由于有红色、白色、蓝色三种颜色，因此需要维护两个段落的左边界。我在这里维护的是红色的右边界r以及白色的右边界w，然后通过r + 1得到白色的左边界，通过w + 1来得到蓝色的左边界。这样做的目的是对于没有红色或者没有白色的情况而言，维护右边界然后计算左边界比直接维护左边界似乎更加方便一些。

首先三种颜色都没有，于是有r \= w \= -1，接下来从左往右扫描，设当前的下标为index：

1、如果当前是蓝色，那么现在的情况就是：

0 0 0 ... 0 0 0(r在这里) 1 1 1 ... 1 1 1(w在这里) 2 2 2 ... 2 2 2 2(index在这里)

于是无事发生。

2、如果当前是白色，那么现在的情况就是：

0 0 0 ... 0 0 0(r在这里) 1 1 1 ... 1 1 1(w在这里) 2 2 2 ... 2 2 2 1(index在这里)

此时需要将最右边的1与最左侧的2互换，变成：

0 0 0 ... 0 0 0(r在这里) 1 1 1 ... 1 1 1(w在这里) 1 2 2 2 ... 2 2 2(index在这里)

可以看到，这里将nums[index]与nums[w + 1]互换即可。交换完成之后需要更新白色的右边界w，即w +\= 1。

3、如果当前是红色，那么现在的情况就是

0 0 0 ... 0 0 0(r在这里) 1 1 1 ... 1 1 1(w在这里) 2 2 2 ... 2 2 2 0(index在这里)

变换之后的情况应该是

0 0 0 ... 0 0 0(r在这里) 0 1 1 ... 1 1 1(w在这里) 1 2 2 ... 2 2 2 2(index在这里)

对比刚开始的状态和最终状态，可以发现nums[index]变成了nums[w + 1]，nums[w + 1]则变成了nums[r + 1]，而nums[r + 1]变成了0。当然，也可以理解为进行了两次交换。

交换完成之后红色与白色的右边界都往后移动了一位，因此需要更新这两个边界，即r +\= 1，w +\= 1。

这样一来，就达到了题目要求的一趟扫描，且仅使用常数的空间的要求了。

最后附上python代码：

```python
class Solution(object):
    def sortColors(self, nums):
        """
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        """

        r = -1
        w = -1

        for index, num in enumerate(nums):
            if num == 2:
                continue
            elif num == 1:
                nums[index] = nums[w + 1]
                nums[w + 1] = 1
                w += 1
            else:
                nums[index] = nums[w + 1]
                nums[w + 1] = nums[r + 1]
                nums[r + 1] = 0
                r += 1
                w += 1
        return nums
```
