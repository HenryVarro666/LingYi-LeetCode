---
title: "1861. 旋转盒子"
aliases: ["yiduobo的每日leetcode 1861.旋转盒子"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/473009555"
zhihu_id: "473009555"
zhihu_title: "yiduobo的每日leetcode 1861.旋转盒子"
question_id: "1861"
question: "旋转盒子"
problem_url: "https://leetcode.cn/problems/rotating-the-box/"
difficulty: "Medium"
rating: 1537
created: "2022-02-26T23:34:37+08:00"
updated: "2022-02-26T23:34:37+08:00"
upvotes: 0
comments: 0
---

# 1861. 旋转盒子

> **[yiduobo的每日leetcode 1861.旋转盒子](https://zhuanlan.zhihu.com/p/473009555) · 知乎 · 2022-02-26 · 赞同 0**
> 力扣：[1861. 旋转盒子](https://leetcode.cn/problems/rotating-the-box/) · Medium · 灵茶山艾府：[两种方法：正序遍历 / 倒序遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1861.旋转盒子

[力扣](https://leetcode-cn.com/problems/rotating-the-box/)

仔细观察可以发现，原始矩阵的第i行对应到的是旋转后的m - i - 1列，且各行各列之间是互补影响的，因此可以从上到下遍历原始矩阵的每一行，将当前行旋转后的结果填充到答案矩阵的第m - i - 1列。

对于其中的某一行，旋转后石头会落下去，那么对应回原始行，就是左侧的石头将被移动到右侧最近的石头或者障碍物旁边。由于在答案列中应该从小往上考虑，因此在原始行中就应该从右往左进行遍历。另外，由于石头会堆起来，因此还需要一个变量p，用来记录最上面被占用的行号。初始状态下，p应该等于n，表示答案列中还没有行被占用。

接下来，对于当前遍历到的格子：

1、若当前格子是障碍物，由于障碍物并不会下落，因此其在原始行中的列j就是其在答案列中的行。同时，其左侧的石头在下落时将被这个障碍物阻挡，因此需要更新p为j。

2、若当前格子是石头，那么其在旋转后将会下落到p的上一行，因此其在答案列中的行就是p - 1，同时需要将p更新为p - 1

3、若当前格子什么都没有，那么就无须处理

最后附上python代码：

```python
class Solution(object):
    def rotateTheBox(self, box):
        """
        :type box: List[List[str]]
        :rtype: List[List[str]]
        """

        m = len(box)
        n = len(box[0])

        res = [['.'] * m for _ in range(n)]
        
        for i in range(m):
            p = n
            for j in range(n - 1, -1, -1):
                if box[i][j] == '*':
                    res[j][m - i - 1] = '*'
                    p = j
                elif box[i][j] == '#':
                    res[p - 1][m - i - 1] = '#'
                    p -= 1
        
        return res
```
