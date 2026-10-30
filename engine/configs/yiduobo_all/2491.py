def _pos(S):
    """当前遍历到 skill 的哪个下标（由已配对数和哈希表里剩余个数反推）"""
    if 'pairs' not in S or 'skill_cnt' not in S:
        return None
    c = 2 * S['pairs'] + sum(S['skill_cnt'].values())
    ln = S['_line']
    return c + 1 if ln == 18 else c - 1 if ln in (19, 21) else c


CONFIG = dict(
    num=2491, title='划分技能点相等的团队', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='总和定目标 · 哈希表边遍历边配对',
    tags=[],
    code='''
class Solution(object):
    def dividePlayers(self, skill):

        n = len(skill)
        s = sum(skill)

        if (s + s) % n != 0:
            return -1

        res = 0
        target = (s + s) // n

        skill_cnt = {}
        pairs = 0
        for sk in skill:
            if skill_cnt.get(target - sk, 0) > 0:
                res += (target - sk) * sk
                skill_cnt[target - sk] -= 1
                pairs += 1
            else:
                skill_cnt[sk] = skill_cnt.get(sk, 0) + 1
        
        if pairs != n // 2:
            return -1
        return res
''',
    call='Solution().dividePlayers([3,2,5,1,3,4])',
    expect=22,
    views=[
        dict(type='array', var='skill', label='skill（蓝 = 当前遍历到的数）', cell=90, h=170,
             color=lambda S, k, v: 'blue' if 'sk' in S and _pos(S) == k else None),
        dict(type='map', var='skill_cnt', label='skill_cnt（还没配对的数 : 个数）', fmt=lambda k, v: f'{k}: {v}', h=170, font=32),
        dict(type='text', size=28, h=70,
             fn=lambda S: (f"目标和 `target = {S['target']}`　已配 `pairs = {S['pairs']}`　化学反应 `res = {S['res']}`"
                           if 'pairs' in S else (f"目标和 `target = {S['target']}`" if 'target' in S else ''))),
    ],
    watch=[('s', 's'), ('target', 'target', 'orange'), ('sk', 'sk', 'blue'), ('pairs', 'pairs', 'pink'), ('res', 'res', 'green')],
    captions={
        's = sum(skill)': '`n = {n}`，所有数之和 `s = {s}`',
        'if (s + s) % n != 0': lambda S, B, ret: (f'`2s = {2*S.s}` 能被 `n = {S.n}` 整除：每队目标和是整数，可以继续'
                                                  if (2 * S.s) % S.n == 0 else '`2s` 不能被 `n` 整除 → 不可能分成等和的队'),
        'return -1': lambda S, B, ret: ('总和对不上，返回 -1' if S.get('pairs') is None else
                                        f'只配出 `{S.pairs}` 对，不等于 `n // 2 = {S.n // 2}` → 有数落单，返回 -1'),
        'target = (s + s)': '`n/2` 队，每队和为 `s ÷ (n/2) = 2s ÷ n`，所以 `target = {target}`',
        'skill_cnt = {}': '`skill_cnt` 记录==还没配对==的数',
        'for sk in skill': lambda S, B, ret: (f'遍历到 `sk = {S.sk}`' if S.pairs + sum(S.skill_cnt.values()) <= len(S.skill) and _pos(S) < len(S.skill) else '遍历结束'),
        'if skill_cnt.get': lambda S, B, ret: (
            f'需要搭档 `target − sk = {S.target - S.sk}`，哈希表里有 `{S.skill_cnt.get(S.target - S.sk, 0)}` 个 → ==配对=='
            if S.skill_cnt.get(S.target - S.sk, 0) > 0 else
            f'需要搭档 `{S.target - S.sk}`，哈希表里没有 → 先记下 `{S.sk}` 等搭档'),
        'res += ': '配对 `{target - sk} × {sk} = {(target - sk) * sk}`，`res` → =={res}==',
        'skill_cnt[target - sk] -= 1': '搭档用掉一个：`skill_cnt[{target - sk}]` → `{skill_cnt[target - sk]}`',
        'pairs += 1': '成功配对数 `pairs` → {pairs}',
        'skill_cnt[sk] = ': '把 `{sk}` 记入哈希表：`skill_cnt = {skill_cnt}`',
        'if pairs != n // 2': lambda S, B, ret: (f'`pairs = {S.pairs}`，`n // 2 = {S.n // 2}`：' + ('一致，全部配上' if S.pairs == S.n // 2 else '不一致 → 有落单的数')),
        'return res': '全部配对成功，返回 =={res}==',
    },
    cards=dict(
        one_liner='总和 ÷ 队数 = 每队目标和，哈希表边扫边配对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['偶数个玩家分成二人队，每队技能点之和==相等==',
                 '队的化学反应 = 技能点乘积，求总和；无法分则返回 `-1`',
                 '示例：`[3,2,5,1,3,4]` → `22`'],
        quote='可以先通过数组的总和处理数组长度的一半来计算出每个二元组中两个数之和应该等于多少，记这个数为target。',
        quote_src='—— yiduobo 题解原文',
        idea=['总和 `s`，队数 `n/2` → `target = s ÷ (n/2)`，不整除就返回 -1',
              '一趟遍历：哈希表里有 `target - sk` 就配对并累加乘积，否则把 `sk` 存进去',
              '最后配对数必须等于 `n/2`，否则有数落单'],
        summary=['时间 `O(n)`，空间 `O(n)`；不需要排序',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（`target` 与 `n // 2` 两处）',
                 '易错：`(s + s) % n` 先乘 2 再取模，避免 `n/2` 的小数',
                 '对比灵神：灵神排序后首尾配对；yiduobo 用哈希表一趟配对'],
    ),
)
