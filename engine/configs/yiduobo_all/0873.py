def _txt(S):
    if 'a' not in S or 'cnt' not in S:
        return '枚举头两项 `arr[i]`、`arr[j]`，用哈希表判断下一项在不在'
    a, b = S['a'], S['b']
    return f'当前末两项 `{a}`, `{b}`：下一项应为 `{a} + {b}` = =={a + b}==，已向后扩展 `{S["cnt"]}` 次'


CONFIG = dict(
    num=873, title='最长的斐波那契子序列的长度', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='枚举头两项 · 哈希表向后扩展',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def lenLongestFibSubseq(self, arr):

        num_set = set(arr)
        n = len(arr)
        res = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                a, b = arr[i], arr[j]
                cnt = 0
                while a + b in num_set:
                    a, b = b, a + b
                    cnt += 1
                if cnt > 0:
                    res = max(res, cnt + 2)
        
        return res
''',
    call='Solution().lenLongestFibSubseq([1,2,3,4,5,8])',
    expect=5,
    max_steps=80,
    views=[
        dict(type='array', var='arr', label='arr（严格递增）', h=215, cell=80,
             pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, k, v: ('blue' if k == S.get('i') else 'pink' if k == S.get('j') else None)),
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='set', var='num_set', label='num_set', h=130, fmt=lambda x: str(x)),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('a', 'a', 'cyan'), ('b', 'b', 'orange'),
           ('cnt', 'cnt', 'yellow'), ('res', 'res', 'green')],
    captions={
        'num_set = set': '把 `arr` 放进哈希集合：`a + b in num_set` 判断一次 `O(1)`',
        'res = 0': '`res` 记录最长斐波那契子序列长度，没有就是 0',
        'for i in range': '枚举第一项的下标 `i`',
        'for j in range': '枚举第二项的下标 `j`',
        'a, b = arr[i], arr[j]': '头两项确定了：`a = {a}`, `b = {b}`，整个数列随之确定',
        'cnt = 0': '`cnt` 记录头两项之后又接上了几项',
        'while a + b in num_set': lambda S, B, r: (f'`{S.a} + {S.b} = {S.a + S.b}` 在 arr 中 → ==继续扩展==' if S.a + S.b in S.num_set
                                                   else f'`{S.a} + {S.b} = {S.a + S.b}` 不在 arr 中 → ==停止扩展=='),
        'a, b = b, a + b': '数列往后挪一位：末两项变成 `{a}`, `{b}`',
        'cnt += 1': '又接上一项：`cnt = {cnt}`',
        'if cnt > 0': lambda S, B, r: (f'`cnt = {S.cnt} > 0`：至少扩展过一次，头两项加后续共 `{S.cnt + 2}` 项' if S.cnt > 0
                                       else '`cnt = 0`：连第三项都接不上，长度不到 3，不算'),
        'res = max': '`res = max({B.res}, {cnt} + 2)` = =={res}==',
        'return res': '最长斐波那契子序列长度 = =={ret}==',
    },
    cards=dict(
        one_liner='头两项一确定，整个斐波那契数列就确定了',
        complexity='时间 `O(n^2 log M)`，空间 `O(n)`',
        problem=['严格递增正整数数组 `arr`，找最长的斐波那契式子序列的长度',
                 '序列长度 `≥ 3`，且 `x[i] + x[i+1] = x[i+2]`；找不到返回 0',
                 '示例：`[1,2,3,4,5,6,7,8]` → `5`（`1,2,3,5,8`）'],
        quote='没有想到什么特别好的处理方法，我的做法是直接枚举数列的头两项，然后向后扩展，同时利用哈希表来判断当前项是否出现在arr当中。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举两个下标 `i < j` 作为头两项 `a`、`b`',
              '只要 `a + b` 在哈希集合里，就==往后接==一项并继续',
              '接不上就停下，`cnt > 0` 时用 `cnt + 2` 更新答案'],
        summary=['暴力枚举：`O(n^2)` 个头两项，每个最多扩展 `O(log M)` 次（数列指数增长）',
                 '易错：`cnt` 只数新接的项，所以长度是 `cnt + 2`',
                 '`cnt = 0` 说明长度不足 3，不能更新答案',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '题单里常见的另一种做法是 DP：`f[j][k]` 表示以 `arr[j], arr[k]` 结尾的长度'],
    ),
)
