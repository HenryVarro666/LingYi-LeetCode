def _f(S):
    if 'j' not in S or 'i' not in S:
        return '`s[i]` = 前 `i` 个房间各自「奇数次到访 → 偶数次回来」所需天数之和'
    i, j, s = S['i'], S['j'], S['s']
    return f'`s[{i + 1}] = 2×s[{i}] − s[{j}] + 2` = 2×{s[i]} − {s[j]} + 2 = =={2 * s[i] - s[j] + 2}=='


CONFIG = dict(
    num=1997, title='访问完所有房间的第一天', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='前缀和优化 DP',
    tags=['灵神题单·动态规划', '前缀和优化 DP', '难度分 2260'],
    code='''
class Solution:
    def firstDayBeenInAllRooms(self, nextVisit: List[int]) -> int:
        s = [0] * len(nextVisit)
        for i, j in enumerate(nextVisit[:-1]):
            s[i + 1] = (s[i] * 2 - s[j] + 2) % 1_000_000_007
        return s[-1]
''',
    call='Solution().firstDayBeenInAllRooms([0,0,1,2,1])',
    expect=20,
    skip=['for i, j in enumerate'],
    views=[
        dict(type='text', h=70, size=24, fn=_f),
        dict(type='array', var='nextVisit', label='nextVisit（i = 当前房间，j = 回访目标 nextVisit[i]）', h=250, cell=100,
             pointers={'i': 'blue', 'j': 'pink'}, window=('j', 'i - 1'),
             color=lambda S, k, v: 'pink' if S.get('j') == k else 'blue' if S.get('i') == k else None),
        dict(type='array', var='s', label='s[i]：访问完前 i 个房间所需天数（前缀和）', h=250, cell=100,
             pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, k, v: 'yellow' if S.get('i') is not None and k == S['i'] + 1 and S.get('_line') == 5 else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('s[-1]', 's[-1]', 'green')],
    captions={
        's = [0] *': '`s[i]` 是前缀和：`s[0] = 0`，其余先占位',
        's[i + 1] =': lambda S, B, r: (f'首次到 `{S.i}` 号房（奇数次）→ 回访 `{S.j}` 号房；`[{S.j}, {S.i - 1}]` 里没有房间要重走，只算本房间进出 2 天：`s[{S.i + 1}] = 2×{B.s[S.i]} − {B.s[S.j]} + 2` = =={S.s[S.i + 1]}==' if S.j > S.i - 1 else f'首次到 `{S.i}` 号房 → 回访 `{S.j}` 号房，`[{S.j}, {S.i - 1}]` 的房间各要再「回访」一遍：`s[{S.i + 1}] = 2×{B.s[S.i]} − {B.s[S.j]} + 2` = =={S.s[S.i + 1]}=='),
        'return s[-1]': '访问完所有房间的日期编号 = `s[n-1]` = =={ret}==',
    },
    cards=dict(
        one_liner='回访 j 要把 [j, i-1] 的房间再走一遍：前缀和直接算',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个房间，第 0 天在 0 号房；到访次数为奇数 → 去 `nextVisit[i]`，偶数 → 去 `i+1`',
                 '求第一次访问完所有房间的日期编号，对 `10^9+7` 取模',
                 '示例：`[0,0,2]` → `6`；本视频：`[0,0,1,2,1]` → `20`'],
        quote='所以要想重新回到 i，对于 [j,i-1] 范围内的每个房间，我们都需要执行一次「回访」。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i]`：从「奇数次到 i」到「偶数次回到 i」要几天',
              '`f[i] = 2 + f[j] + … + f[i-1]`，和式用前缀和 `s` 化简',
              '联立 `s[i+1] = s[i] + f[i]` 得 `s[i+1] = 2·s[i] − s[j] + 2`，省掉 `f`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '答案是 `s[n-1]`：天数 `s[n-1]+1` 再减去从第 0 天起算的 1',
                 '`nextVisit[n-1]` 没用到，所以循环只走 `nextVisit[:-1]`',
                 'Python 取模结果非负，减 `s[j]` 不用额外加 `MOD`'],
    ),
)
