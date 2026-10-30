def _weak(S, i):
    """bonus 不够大的位置"""
    b = S.get('bonus')
    return b is not None and i < len(b) and len(b) == len(S['monsters']) and b[i] < S['monsters'][i]


def _txt(S):
    if 'bonus' not in S or len(S['bonus']) < len(S['monsters']):
        return '先用差分数组算出每个位置的总加成 `bonus`'
    if S['_line'] < 15:
        return '`bonus[i] < monsters[i]` 的位置（橙色）才需要初始强度'
    i = S.get('index')
    if i is None:
        return ''
    m, b = S['monsters'][i], S['bonus'][i]
    if b < m:
        return f"位置 `{i}`：最小初始强度 = `sum(monsters[:{i + 1}]) − bonus[{i}]` = `{sum(S['monsters'][:i + 1])} − {b}` = =={sum(S['monsters'][:i + 1]) - b}=="
    return f"位置 `{i}`：加成 `{b}` >= 怪物 `{m}`，靠加成就能过，继续往前找"


CONFIG = dict(
    num=4008, title='击败所有怪物的最小初始强度', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='差分数组 + 倒序找最后一个加成不足的位置',
    tags=['二分答案', '一维 DP', '难度分 1776'],
    code='''
class Solution(object):
    def minInitialStrength(self, monsters, boosts):
        
        n = len(monsters)
        f = [0] * n
        for left, right, v in boosts:
            f[left] += v
            if right + 1 < n:
                f[right + 1] -= v
        
        bonus = [f[0]]
        for index in range(1, n):
            bonus.append(bonus[-1] + f[index])
        
        for index in range(n - 1, -1, -1):
            if bonus[index] < monsters[index]:
                return sum(monsters[:index + 1]) - bonus[index]
        
        return 0
''',
    call='Solution().minInitialStrength([3,6,2,5,4], [[1,1,2],[3,4,6]])',
    expect=11,
    views=[
        dict(type='text', size=24, fn=_txt),
        dict(type='array', var='monsters', label='monsters', h=240,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if S.get('index') == i and S['_line'] >= 15 else None),
        dict(type='array', var='bonus', label='bonus（橙 = 加成不够，bonus[i] < monsters[i]）', h=240,
             color=lambda S, i, v: 'orange' if _weak(S, i) and S['_line'] >= 14 else None),
    ],
    watch=[('index', 'index', 'blue'), ('n', 'n')],
    captions={
        'f[left] += v': '差分：区间 `[{left}, {right}]` 加成 `{v}` → `f[{left}] += {v}`',
        'f[right + 1] -= v': '`f[{right + 1}] -= {v}`：区间之后抵消（`right + 1` 没越界才写）',
        'bonus = [f[0]]': '前缀和开始：`bonus[0] = {f[0]}`',
        'bonus.append': '`bonus[{index}]` = =={bonus[index]}==：第 `{index}` 个怪物战斗时的总加成',
        'for index in range(n - 1, -1, -1)': lambda S, B, r: ('倒序找：最靠后的、加成不够大的位置，所需强度最大' if B.get('index') == S.index and S.index == len(S.monsters) - 1
                                                              else (f'位置 `{S.index}`' if B.get('index') != S.index else '没有加成不够的位置')),
        'if bonus[index] < monsters[index]': lambda S, B, r: (f"`bonus[{S.index}] = {S.bonus[S.index]} < monsters[{S.index}] = {S.monsters[S.index]}`"
                                                              f" → 加成不够大，需要初始强度" if S.bonus[S.index] < S.monsters[S.index] else
                                                              f"`bonus[{S.index}] = {S.bonus[S.index]} >= monsters[{S.index}] = {S.monsters[S.index]}`"
                                                              f" → 靠加成就能过，强度需求取决于更前面的位置"),
        'return sum(': '`sum(monsters[:{index + 1}]) − bonus[{index}]` = `{sum(monsters[:index + 1])} − {bonus[index]}` → ==答案 {sum(monsters[:index + 1]) - bonus[index]}==',
        'return 0': '每个位置的加成都够 → 初始强度 0 就行',
    },
    cards=dict(
        one_liner='只看最靠后那个「加成不够」的位置：前面怪物总和 − 它的加成',
        complexity='时间 `O(n + m)`，空间 `O(n)`',
        problem=['`monsters[i]` 是怪物强度，`boosts` 里 `[l, r, v]` 给 `[l, r]` 的怪物战斗时加成 `v`',
                 '强度 + 加成 `>= monsters[i]` 才能击败，击败后强度减 `monsters[i]`（负数置 0）',
                 '求打败全部怪物的最小初始强度',
                 '示例：`[5,10,15], [[1,1,10]]` → `30`'],
        quote='其中最大值显然就是最靠后的那一个：对于所有bonus不够大的位置，其中初始所需强度最大的位置必然是最靠后的那个。',
        quote_src='—— yiduobo 题解原文',
        idea=['差分数组 + 前缀和得到每个位置的 `bonus`',
              '`bonus[i] >= monsters[i]` 的位置不拖累后面；否则到达位置 i 前至少要 `s[i] − bonus[i]` 初始强度',
              '证明：靠后位置 q 的需求 `> s[q−1] >= s[p]` >= 靠前位置 p 的需求 → 取最后一个',
              '倒序遍历，遇到第一个加成不够的位置就返回'],
        summary=['时间 `O(n + m)`，空间 `O(n)`',
                 '差分时 `right + 1` 可能等于 `n`，要先判断是否越界',
                 '若没有任何加成不足的位置，答案是 `0`',
                 '对比灵神：灵神用 `f_i` 逆向递推，或二分答案；yiduobo 直接证明「最后一个不足位置」最大'],
    ),
)
