---
title: "3630. 划分数组得到最大异或运算和与运算之和"
aliases: ["yiduobo的每日leetcode 3630.划分数组得到最大异或运算和与运算之和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/math", "leetcode/dynamic-programming", "leetcode/enumeration", "题单/位运算", "题单/位运算/七-线性基"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1945950594863980896"
zhihu_id: "1945950594863980896"
zhihu_title: "yiduobo的每日leetcode 3630.划分数组得到最大异或运算和与运算之和"
question_id: "3630"
question: "划分数组得到最大异或运算和与运算之和"
problem_url: "https://leetcode.cn/problems/partition-array-for-maximum-xor-and-and/"
difficulty: "Hard"
rating: 2744
created: "2025-09-01T21:57:55+08:00"
updated: "2025-09-01T21:57:55+08:00"
upvotes: 1
comments: 0
---

# 3630. 划分数组得到最大异或运算和与运算之和

> **[yiduobo的每日leetcode 3630.划分数组得到最大异或运算和与运算之和](https://zhuanlan.zhihu.com/p/1945950594863980896) · 知乎 · 2025-09-01 · 赞同 1**
> 力扣：[3630. 划分数组得到最大异或运算和与运算之和](https://leetcode.cn/problems/partition-array-for-maximum-xor-and-and/) · Hard · 灵茶山艾府：[式子变形 + 线性基 + 最优性剪枝（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3630.划分数组得到最大异或运算和与运算之和

[3630. 划分数组得到最大异或运算和与运算之和 - 力扣（LeetCode）](https://leetcode.cn/problems/partition-array-for-maximum-xor-and-and/description/)

题目给出一个整数数组nums，其长度不超过20。现在要求将其划分为三个子序列A、B和C，子序列可以为空，使得XOR(A) + AND(B) + XOR(C)最大。其中XOR(arr)表示arr中所有元素的按位异或结果，AND(arr)则表示arr中所有元素按位与结果。

题目的名字比较拗口，实际上就是要求将一个数组nums划分成三个部分A、B、C，要求A的按位异或，加上B的按位与，加上C的按位异或，这三者之和最大。

nums的数据规模并不大，但是划分起来是比较困难的。一个直观的想法就是让B中的元素尽量少，因为按位与是越来越小的，但是从样例3中可以看出，为了兼顾异或的结果，B中的元素也并不是必然只有一个，因此在这里还是只能通过枚举来做。

朴素的枚举的时间复杂度为3^n，因为每个元素都可能属于其中一个部分，在当前n \= 20的情况下显然是不行，需要进行优化。注意到A和C都是按位异或，也许存在某种优化的可能，因此在这里可以考虑枚举B中有哪些元素，然后考虑剩下元素组成A和C时可能得到的最优划分是什么。

枚举B中元素的时间复杂度为2^n，也就是每个元素是否属于B，这个时间复杂度是可以接受的，那么接下来的问题就是如何高效找出划分A和C的方法，使得XOR(A)与XOR(C)之和最大。

更具体的说，问题就转化成了给出一个数组arr，要求将其划分为两个部分，这两个部分的异或值之和最大。

在划分之前，有一个前提是XOR(A) ^ XOR(C) \= XOR(arr)，也就是这两个部分的异或值，再进行异或得到的结果是固定的，即XOR(arr)。

如果从二进制的角度来考虑，对于XOR(arr)中值为1的某个位p，其必然是由一个0和一个1异或得来的，而这个1无论是属于XOR(A)还是XOR(C)，其对XOR(A) + XOR(C)的贡献都是2^p；反之，对于其中值为0的某个为p，其要么是两个0异或得到的，要么是两个1异或得到的，而为了使得XOR(A)与XOR(C)之和最大，就应该尽量让XOR(arr)中高位的0拆分成两个1。为了消除XOR(arr)中值为1的位的影响，在这里可以先将arr中的所有元素都消除掉XOR(arr)中值为1的位，也就是说对于其中的每个元素x，都应该将其与x & XOR(arr)执行一次异或操作，方便起见，记异或后的数组为ac。

到了这里，问题就变成了从ac中选出一些元素，使得这些元素的异或值最大，而这个最大的异或值乘以2，再加上XOR(arr)，就是将arr分为A和C后XOR(A) + XOR(C)的最大值。

直观来说，这个问题依然需要使用2^n的复杂度枚举子集来进行计算，但是之前枚举B的复杂度已经是2^n了，在这里必须来点高级货进行优化。

对于子集异或最大问题，通常可以使用异或线性基来进行求解。异或线性基指的是一组线性无关的数，这些数可以通过异或操作还原出原集合中的所有元素。对于异或线性基的求解，可以从二进制的最高位开始向低位遍历，逐位进行填充。令f[index]表示线性基中二进制最高位的1处于index这一位时的数是什么，那么对于ac中的每个元素x，从大到小遍历二进制位index：

1、若x在index这一位上为1，且f[index]为空，此时就将f[index]置为x

2、若x在index这一位上为1，且f[index]不为空，此时让x异或f[index]

3、若x在index这一位上不为1，则直接跳过这一位

得到f数组后，就只需从高位到低位再进行一次遍历，对于当前的异或结果v，若v在index这一位上为0，且f[index]非空，那么就让v异或上f[index]。基于f[index]的定义，f[index]在index + 1或者更高位上都为0，因此不会影响到之前更高位上的结果，在这个前提下，将v与f[index]异或，从而让index这一位变为1必然是更优的。

到了这里，就可以在O(n \* logv)的时间内计算出ac的最大异或值，从而在O(2^n \* n \* logv)的复杂内计算出原问题的答案了。

最后附上python代码：

```python
class Solution(object):
    def maximizeXorAndXor(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        n = len(nums)

        def calc(ac):
            if not ac:
                return 0
            length = len(bin(max(ac))) - 2
            f = [None] * (length + 1)
            for x in ac:
                for index in range(length, -1, -1):
                    if x & (1 << index) == (1 << index):
                        if f[index] is None:
                            f[index] = x
                            break
                        else:
                            x ^= f[index]

            best = 0
            for index in range(length, -1, -1):
                if f[index] and (best & (1 << index) == 0):
                    best ^= f[index]
            
            return best

        for state in range(1 << n):
            b = None
            ac = []
            xor = 0
            s = 0
            for index in range(n):
                if state & (1 << index) == (1 << index):
                    if b is None:
                        b = nums[index]
                    else:
                        b &= nums[index]
                else:
                    ac.append(nums[index])
                    s += nums[index]
                    xor ^= nums[index]
            
            if b is None:
                b = 0

            if s + b <= res:
                continue

            s = 0
            for index, v in enumerate(ac):
                ac[index] = v ^ (v & xor)
                s += ac[index]

            if s * 2 + xor + b <= res:
                continue

            res = max(res, b + calc(ac) * 2 + xor)

        return res
```
