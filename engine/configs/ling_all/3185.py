_P = 'sum(cnt) - (_line == 10) if _line != 11 else None'
_NEED = '(H - t % H) % H if _line == 9 else None'
_ME = 't % H if _line == 10 else None'


def _txt(S):
    if 't' not in S or S.get('_line') == 11:
        return '`cnt[r]`：左边模 24 余 `r` 的个数'
    t = S['t']
    r = t % 24
    return f"`t = {t}`，`t % 24 = {r}` → 要找左边余 `(24 − {r}) % 24` = =={(24 - r) % 24}=="


CONFIG = dict(
    num=3185, title='构成整天的下标对数目 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 模 24 计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1010'],
    code='''
class Solution:
    def countCompleteDayPairs(self, hours: List[int]) -> int:
        H = 24
        ans = 0
        cnt = [0] * H
        for t in hours:
            # 先查询 cnt，再更新 cnt，因为题目要求 i < j
            # 如果先更新，再查询，就把 i = j 的情况也考虑进去了
            ans += cnt[(H - t % H) % H]
            cnt[t % H] += 1
        return ans
''',
    call='Solution().countCompleteDayPairs([12,12,30,24,24,48,18])',
    expect=5,
    views=[
        dict(type='array', var='hours', label='hours（t = 当前枚举的右端）', pointers={_P: 'blue'}, pointer_labels={_P: 't'}, h=200,
             dim=lambda S, i, v: 'cnt' in S and S.get('_line') != 11 and i > sum(S['cnt']) - (S.get('_line') == 10)),
        dict(type='array', var='cnt', label='cnt（下标 = 余数）', cell=40, h=200,
             pointers={_NEED: 'green', _ME: 'pink'}, pointer_labels={_NEED: '查', _ME: '+1'},
             dim=lambda S, i, v: v == 0),
        dict(type='text', fn=_txt, h=90, size=30),
    ],
    watch=[('t', 't', 'blue'), ('t % 24', 't % H'), ('ans', 'ans', 'green')],
    captions={
        'H = 24': '一天 `H = 24` 小时，只关心 `t % 24`',
        'ans = 0': '`ans` 统计下标对数',
        'cnt = [0] * H': '`cnt[r]`：左边模 24 余 `r` 的数有几个',
        'for t in hours': lambda S, B, r: (f'枚举右端 `t = {S.t}`，把它看成常量' if sum(S.cnt) < len(S.hours) else '遍历结束'),
        'ans += cnt': lambda S, B, r: (
            (f'`t % 24 = 0`：再 `% H` 后要找余 ==0== 的，左边有 `{S.cnt[0]}` 个 → `ans = {S.ans}`' if S.t % 24 == 0
             else f'`{S.t % 24} + {24 - S.t % 24} = 24`：左边余 =={24 - S.t % 24}== 的有 `{S.cnt[24 - S.t % 24]}` 个 → `ans = {S.ans}`')),
        'cnt[t % H] += 1': '查询完再计入自己：`cnt[{t % H}]` → `{cnt[t % H]}`',
        'return ans': '一共 `{ans}` 对',
    },
    cards=dict(
        one_liner='枚举右边的 t，查左边有几个余数能补成 24 的倍数',
        complexity='时间 `O(n + H)`，空间 `O(H)`，`H = 24`',
        problem=['求 `i < j` 且 `hours[i] + hours[j]` 是 ==24 的倍数== 的下标对数',
                 '示例：`[12,12,30,24,24]` → `2`',
                 '本视频：`[12,12,30,24,24,48,18]` → `5`'],
        quote='一般地，对于 hours[i]，需要知道左边有多少个模 24 是 24 − hours[i] mod 24 的数。特别地，如果 hours[i] 模 24 是 0，那么需要知道左边有多少个模 24 ==也是 0== 的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['和两数之和一样：==枚举右，维护左==',
              '两种情况合并成 `(H − t % H) % H` 一个下标',
              '`cnt` 只要 24 个格子，`hours[i]` 再大也没关系'],
        summary=['时间 `O(n + H)`，空间 `O(H)`',
                 '易错：余 0 时 `H − 0 = 24` 越界，外面要再 `% H`',
                 '先查询再更新：否则会把 `i = j` 算进去',
                 '同类题：1010（模 60）、3184（数据范围小的版本）'],
    ),
)
