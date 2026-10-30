CONFIG = dict(
    num=1711, title='大餐计数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表 · 枚举 2 的幂',
    code='''
class Solution:
    def countPairs(self, deliciousness):

        pow2 = [1]
        num_dict = {}
        for v in deliciousness:
            num_dict[v] = num_dict.get(v, 0) + 1
            while pow2[-1] <= v:
                pow2.append(pow2[-1] + pow2[-1])
        
        mod = 10 ** 9 + 7
        res = 0

        for v, cnt in num_dict.items():
            for p in pow2:
                if v + v == p:
                    res += cnt * (cnt - 1) // 2 % mod
                elif v + v < p:
                    res += cnt * num_dict.get(p - v, 0) % mod
                    
        return res
''',
    call='Solution().countPairs([1,1,3,7])',
    expect=5,
    views=[
        dict(type='array', var='deliciousness', label='deliciousness', h=150,
             color=lambda S, i, v: 'blue' if S.get('v') == v else None),
        dict(type='array', var='pow2', label='pow2（候选的和）', h=150,
             color=lambda S, i, v: 'pink' if S.get('p') == v and 'cnt' in S else None),
        dict(type='map', var='num_dict', label='num_dict：数值 → 出现次数', h=170),
        dict(type='text', h=70, fn=lambda S: (
            f"枚举 `v={S['v']}`（出现 {S['cnt']} 次）和 `p={S['p']}`：另一半是 `{S['p']} − {S['v']} = {S['p']-S['v']}`"
            if 'p' in S and 'cnt' in S else '')),
    ],
    watch=[('v', 'v', 'blue'), ('cnt', 'cnt', 'cyan'), ('p', 'p', 'pink'), ('res', 'res', 'green')],
    captions={
        'num_dict[v] =': '`{v}` 出现次数记为 `{num_dict[v]}`',
        'while pow2[-1] <= v': lambda S, B, r: (f'`pow2` 末尾 `{S.pow2[-1]}` ≤ `{S.v}`：2 的幂还不够大，继续翻倍'
                                                if S.pow2[-1] <= S.v else f'`pow2` 末尾 `{S.pow2[-1]}` > `{S.v}`：够大了，停止'),
        'pow2.append': '补一个更大的 2 的幂：`pow2` = {pow2}',
        'mod =': '答案取模 `10^9+7`',
        'for v, cnt in': '取一个数值 `{v}`，它出现 `{cnt}` 次；它当较小的那一半',
        'for p in pow2': '试和为 `{p}`',
        'if v + v == p': lambda S, B, r: (f'`{S.v}+{S.v} = {S.p}`：两个数相等，只能在 `{S.cnt}` 个里选 2 个' if S.v + S.v == S.p
                                         else f'`{S.v}+{S.v} = {S.v*2}` ≠ `{S.p}`'),
        'res += cnt * (cnt - 1)': '同值配对 `C({cnt},2) = {cnt*(cnt-1)//2}` → `res` = =={res}==',
        'elif v + v < p': lambda S, B, r: (f'`{S.v*2} < {S.p}`：另一半 `{S.p-S.v}` 比 v 大，只在这里算一次，不重复' if S.v * 2 < S.p
                                         else f'`{S.v*2} ≥ {S.p}`：另一半会比 v 小，已经被小的那个数算过，跳过'),
        'res += cnt * num_dict.get': '`{cnt}` × `num_dict.get({p-v}, 0)` = `{cnt*num_dict.get(p-v,0)}` → `res` = =={res}==',
        'return res': '一共 `{res}` 种大餐',
    },
    cards=dict(
        one_liner='和只可能是 2 的幂，而且最多 22 个，枚举它们再查哈希表',
        complexity='时间 `O(n·log max)`，空间 `O(n)`',
        problem=['`deliciousness[i]` 是第 i 道菜的美味程度，大餐 = 两道不同的菜，美味程度之和是 ==2 的幂==',
                 '求不同大餐的数量，对 `10^9+7` 取模（下标不同就算不同）',
                 '示例：`[1,1,3,7]` → `5`'],
        quote='设数组中的最大值为max，p为满足2^p > max的最小的p，那么必然就有max + x < 2^(p + 1)，最后只需要考察2^0到2^p这些美味程度之和了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先用哈希表数出每个数值的次数，同时造出够大的 2 的幂表 `pow2`',
              '对每个数值 `v` 和每个 `p`：配对数值是 `p - v`，次数相乘 `cnt1 * cnt2`',
              '只在 `v + v < p` 时计数避免重复；`v + v == p` 时是同值内部选 2 个'],
        summary=['时间 `O(n·log max)`，`pow2` 最多 22 项，空间 `O(n)`',
                 '`v + v == p` 要用组合数 `cnt*(cnt-1)/2`，不能乘自己',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，类声明 `Solution(object)` 改为 `Solution`'],
    ),
)
