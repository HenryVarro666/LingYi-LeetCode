T0 = [6, 4, 8, 1, 3, 2]
A0 = [4, 7, 6, 2, 3, 8, 1]


def _arr_color(S, i, v):
    if S.get('num') is None or S.get('_line', 0) < 9:
        return None
    if v == S['num'] and S['num'] in S['target']:
        return 'blue'
    if v == S['num']:
        return 'red'
    return None


def _hint(S):
    ln = S.get('_line', 0)
    f = S.get('f', [])
    if ln < 9:
        return '`pos[x]` = x 在 target 里的位置；把 arr 换成 pos，再求最长上升子序列'
    if S.get('num') is None:
        return ''
    if S['num'] not in S['target']:
        return f"`{S['num']}` 不在 target 里，不可能进公共子序列 → ==跳过=="
    p = S['pos_dict'][S['num']]
    return f"`arr` 当前数 `{S['num']}` → `pos = {p}`；`f` = {f}（长度 {len(f)}）"


CONFIG = dict(
    num=1713, title='得到子序列的最少操作次数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='LCS 转 LIS · 贪心 + 二分',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def minOperations(self, target, arr):

        pos_dict = {}
        for index, num in enumerate(target):
            pos_dict[num] = index

        f = []
        for num in arr:
            if num in pos_dict:
                pos = pos_dict[num]
                if not f or pos > f[-1]:
                    f.append(pos)
                else:
                    l = 0
                    r = len(f) - 1
                    while l < r:
                        mid = (l + r) >> 1
                        if f[mid] < pos:
                            l = mid + 1
                        else:
                            r = mid

                    f[l] = pos

        return len(target) - len(f)
''',
    call=f'Solution().minOperations({T0!r}, {A0!r})',
    expect=3,
    skip=['pos_dict = {}', 'f = []', 'for index, num in enumerate'],
    max_steps=90,
    views=[
        dict(type='array', var='target', label='target（下标 = pos，每个数唯一）', h=150, cell=80),
        dict(type='array', var='arr', label='arr（蓝 = 当前数，红 = 不在 target 里）', h=150, cell=80, color=_arr_color, index=False),
        dict(type='text', fn=_hint, size=24, h=60),
        dict(type='array', var='f', label='f：长度 k 的上升序列的最小结尾 pos', h=190, cell=90,
             pointers={'l if 15 <= _line <= 24 else None': 'blue', 'r if 15 <= _line <= 22 else None': 'pink',
                       'mid if 18 <= _line <= 22 else None': 'yellow'},
             color=lambda S, i, v: 'yellow' if S.get('pos') is not None and v == S['pos'] and S.get('_line', 0) in (13, 24) else None),
    ],
    watch=[('num', 'num', 'blue'), ('pos', 'pos', 'cyan'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('len(f)', 'len(f)', 'green')],
    captions={
        'pos_dict[num] = index': '`pos_dict[{num}] = {index}`：target 的数互不相同，数 ↔ 位置一一对应',
        'for num in arr': lambda S, B, r: (f'取 arr 的下一个数 `{S.num}`' if S.get('num') != B.get('num') else '`arr` 扫完了'),
        'if num in pos_dict': lambda S, B, r: (f'`{S.num}` 在 target 里 → 可能进公共子序列' if S.num in S.pos_dict
                                               else f'`{S.num}` 不在 target 里 → ==不可能==属于公共子序列，直接跳过'),
        'pos = pos_dict[num]': '`{num}` 在 target 里的位置 `pos = {pos}`',
        'if not f or pos > f[-1]': lambda S, B, r: ('`f` 还是空，直接放进去' if not S.f
                                                    else (f'`pos = {S.pos} > f[-1] = {S.f[-1]}` → 能接在最长的序列后面，==长度 +1==' if S.pos > S.f[-1]
                                                          else f'`pos = {S.pos} ≤ f[-1] = {S.f[-1]}` → 接不上末尾，二分找第一个 ≥ pos 的位置去替换')),
        'f.append(pos)': '`f` 末尾加入 `{pos}` → {f}',
        'l = 0': '二分区间 `[l, r]` 在 `f` 里找第一个 `≥ pos` 的位置',
        'r = len(f) - 1': '`r = {r}`',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`，继续二分' if S.l < S.r else f'`l = r = {S.l}`：找到了替换位置'),
        'mid = (l + r) >> 1': '`mid = ({l} + {r}) >> 1 = {mid}`',
        'if f[mid] < pos': lambda S, B, r: (f'`f[{S.mid}] = {S.f[S.mid]} < pos = {S.pos}` → 太小，答案在右边' if S.f[S.mid] < S.pos
                                            else f'`f[{S.mid}] = {S.f[S.mid]} ≥ pos = {S.pos}` → 可能就是它，往左收缩'),
        'l = mid + 1': '`l` → {l}',
        'r = mid': '`r` → {r}',
        'f[l] = pos': lambda S, B, r: f'`f[{S.l}] = {B.f[S.l]}` 换成 `{S.pos}`：==长度不变，但结尾更小==，后面更容易接上 → {S.f}',
        'return len(target)': '最长公共子序列长 `len(f) = {len(f)}`；需要操作 `{len(target)} − {len(f)}` = =={ret}==',
    },
    cards=dict(
        one_liner='target 无重复：把 arr 换成位置序列，LCS 变成 LIS',
        complexity='时间 `O(n log n)`，空间 `O(m)`',
        problem=['`target` 的数互不相同；每次操作可以在 `arr` 任意位置插入任意整数',
                 '求让 `target` 成为 `arr` 的子序列的最少操作数',
                 '示例：`target=[6,4,8,1,3,2]`，`arr=[4,7,6,2,3,8,6,1]` → `3`',
                 '本视频：`arr=[4,7,6,2,3,8,1]` → `3`'],
        quote='target中的数与其在target中的位置是一一对应的。……为了使得这个式子最长，那么就相当于在pos[arr[*]]这个数组上求解==最长上升子序列==。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案 = `m − LCS`；普通 LCS 是 `O(mn)`，数据太大不行',
              '`target` 无重复 → 每个数有唯一的 `pos`；公共子序列的 `pos` 必然严格递增',
              '把 `arr` 里不在 `target` 的数删掉，其余换成 `pos`，求 LIS',
              'LIS 用贪心 + 二分：`f[k]` 存长度 k+1 的序列的最小结尾'],
        summary=['时间 `O(n log n)`，空间 `O(m)`',
                 '易错：`arr` 里不在 `target` 的数要先排除，不能当成 pos',
                 '`f` 不是真正的 LIS，只是长度对；长度 = `len(f)`',
                 '二分找的是第一个 `≥ pos` 的位置（严格上升）',
                 '原文无需改动，直接是 Python 3 可运行的写法'],
    ),
)
