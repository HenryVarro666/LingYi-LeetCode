CONFIG = dict(
    num=1940, title='排序数组之间的最长公共子序列', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='多指针 · 以第一个数组为准',
    tags=[],
    code='''
class Solution(object):
    def longestCommonSubsequence(self, arrays):

        n = len(arrays)
        p = [0] * n
        res = []
        while True:
            target = arrays[0][p[0]]
            end_flag = False
            same_flag = True
            for index in range(1, n):
                while p[index] < len(arrays[index]) and arrays[index][p[index]] < target:
                    p[index] += 1
                
                if p[index] == len(arrays[index]):
                    end_flag = True
                    break
                
                if arrays[index][p[index]] != target:
                    same_flag = False
                    break
            
            if end_flag:
                break
            
            if same_flag:
                res.append(target)
            
            p[0] += 1
            if p[0] == len(arrays[0]):
                break
        
        return res
''',
    call='Solution().longestCommonSubsequence([[1,3,4,6],[1,4,6,7],[2,4,6,9]])',
    expect=[4, 6],
    views=[
        dict(type='array', var=lambda S: S['arrays'][0], label='arrays[0]（逐个当 target）', h=140,
             color=lambda S, i, v: 'blue' if 'p' in S and i == S['p'][0] else None),
        dict(type='array', var=lambda S: S['arrays'][1], label='arrays[1]', h=140,
             color=lambda S, i, v: 'pink' if 'p' in S and i == S['p'][1] else None),
        dict(type='array', var=lambda S: S['arrays'][2], label='arrays[2]', h=140,
             color=lambda S, i, v: 'pink' if 'p' in S and i == S['p'][2] else None),
        dict(type='array', var='res', label='res（公共子序列）', h=140),
    ],
    watch=['p', ('target', 'target', 'blue'), ('index', 'index', 'orange'), 'end_flag', 'same_flag'],
    captions={
        'n = len': '`n = {n}` 个数组',
        'p = [0] * n': '每个数组一个指针 `p[i]`：指向 ==第一个 ≥ target== 的位置，只增不减',
        'res = []': '`res` 存公共元素',
        'target = ': '答案一定都在 `arrays[0]` 里 → 取 `arrays[0][{p[0]}] = {target}` 当目标',
        'end_flag = False': '`end_flag`：某个数组被耗尽',
        'same_flag = True': '`same_flag`：目前所有数组都含有 target',
        'for index': '检查第 `{index}` 个数组',
        'while p[index] <': lambda S, B, r: (f"`arrays[{S.index}][{S.p[S.index]}] = {S.arrays[S.index][S.p[S.index]]}` < target `{S.target}` → 太小，指针右移" if S.p[S.index] < len(S.arrays[S.index]) and S.arrays[S.index][S.p[S.index]] < S.target else f"这个数组已经没有比 `{S.target}` 小的数了，停下"),
        'p[index] += 1': '`p[{index}]` → {p[index]}',
        'if p[index] == len': lambda S, B, r: ("指针走出数组：后面不可能再有公共元素，==全部结束==" if S.p[S.index] == len(S.arrays[S.index]) else "还没走出数组"),
        'end_flag = True': '`end_flag = True`',
        'if arrays[index][p[index]] != target': lambda S, B, r: (f"`arrays[{S.index}][{S.p[S.index]}] = {S.arrays[S.index][S.p[S.index]]}` ≠ `{S.target}` → target 不在这个数组里" if S.arrays[S.index][S.p[S.index]] != S.target else f"`{S.arrays[S.index][S.p[S.index]]}` == `{S.target}`，这个数组里有"),
        'same_flag = False': '`same_flag = False`：这个 target 不是公共元素，不用检查剩下的数组',
        'if end_flag': '`end_flag = {end_flag}`' ,
        'if same_flag': lambda S, B, r: (f"每个数组都含有 `{S.target}` → ==是公共元素==" if S.same_flag else f"`{S.target}` 不是公共元素，跳过"),
        'res.append': '`res` 加入 `{target}` → {res}',
        'p[0] += 1': '换 `arrays[0]` 里的下一个数当 target：`p[0]` → {p[0]}',
        'if p[0] == len': lambda S, B, r: ("`arrays[0]` 遍历完，结束" if S.p[0] == len(S.arrays[0]) else "`arrays[0]` 还有数，继续"),
        'return res': '最长公共子序列 `{res}`',
    },
    cards=dict(
        one_liner='答案一定在第一个数组里：逐个检查它的数在不在其他数组里',
        complexity='时间 `O(总长度)`，空间 `O(n)`',
        problem=['给 `n` 个严格递增的整数数组，求它们的最长公共子序列',
                 '即在每个数组里都出现过的整数，按升序返回',
                 '本视频：`[[1,3,4,6],[1,4,6,7],[2,4,6,9]]` → `[4, 6]`'],
        quote='最终答案一定完整地出现在了array[0]中，因此可以遍历一趟array[0]，检测其中的每个数字是否都在其他的array中出现过。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个数组一个指针 `p[i]`：第一个 `≥ target` 的下标',
              'target 随 `arrays[0]` 递增，所以各指针只往右走，均摊 `O(1)`',
              '所有数组该位置的值都等于 target → 加入答案'],
        summary=['时间 `O(总元素数)`，空间 `O(n)`',
                 '易错点：指针走出任一数组就要立刻结束',
                 '`same_flag` 为假时不用再检查其余数组',
                 '本题原题面库里缺失，题意据 yiduobo 原文与 LeetCode 原题整理；代码无需改动'],
    ),
)
