def _txt(S):
    if 'k' in S and 'd' in S and 's' in S:
        return f'第 {S["a"].index((S["k"], S["d"])) + 1} 个敌人：累计秒数 `s = {S["s"]}`，伤害 `d = {S["d"]}` → 这段扣血 =={S["s"] * S["d"]}=='
    return '敌人 `(k, d)`：k = 击杀所需攻击次数，d = 每秒伤害；按 `k/d` 从小到大打'


def _cur(S):
    if 'k' in S and 'd' in S and 'ans' in S and 'a' in S and (S['k'], S['d']) in S['a']:
        return S['a'].index((S['k'], S['d']))
    return None


CONFIG = dict(
    num=3273, title='对 Bob 造成的最少伤害', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='交换论证 · 按 k/damage 排序',
    tags=['灵神题单', '难度分 2013'],
    code='''
class Solution:
    def minDamage(self, power: int, damage: List[int], health: List[int]) -> int:
        a = [((h - 1) // power + 1, d) for h, d in zip(health, damage)]
        a.sort(key=lambda p: p[0] / p[1])

        ans = s = 0
        for k, d in a:
            s += k
            ans += s * d
        return ans
''',
    call='Solution().minDamage(4, [1,2,3,4], [4,5,6,8])',
    expect=39,
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='array', var='a', cell=130, h=240, label='a = [(k, damage)]',
             color=lambda S, i, v: 'yellow' if _cur(S) == i else None,
             dim=lambda S, i, v: _cur(S) is not None and i < _cur(S)),
        dict(type='text', fn=lambda S: ('排序键 `k/d`：' + '，'.join(f'{k}/{d}={k/d:.2f}' for k, d in S['a'])) if 'a' in S else '', h=80),
    ],
    watch=[('s', 's', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'a = [': '`k = (health - 1) // power + 1` 是击杀所需的攻击次数（上取整）：`a` = {a}',
        'a.sort': '按 `k/damage` 从小到大排序：==又脆又疼的先打==。`a` = {a}',
        'ans = s = 0': '`s` 是从开始到击败当前敌人经过的秒数，`ans` 累计伤害',
        'for k, d': '按 `k/d` 从小到大取下一个敌人：击杀需 `k = {k}` 次攻击，每秒伤害 `d = {d}`',
        's += k': '再花 `{k}` 秒击败这个敌人 → 累计 `s = {s}`',
        'ans += s * d': '这 `{s}` 秒里它一直在打我：`{s} × {d} = {s * d}` → `ans = {ans}`',
        'return ans': '最少总伤害：`{ans}`',
    },
    cards=dict(
        one_liner='先杀又脆又疼的：按 k/damage 从小到大排序',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每秒每个活着的敌人都对 Bob 造成 damage，之后 Bob 攻击一个敌人，血量 −power',
                 '求消灭所有敌人前受到的最少总伤害',
                 '示例：`power=4, damage=[1,2,3,4], health=[4,5,6,8]` → `39`'],
        quote='优先消灭 k/damage 更小的敌人。结合你玩过的某些游戏，应当优先消灭那个又脆皮伤害又高的敌人。',
        quote_src='—— 灵茶山艾府题解',
        idea=['集中火力一个个打，比雨露均沾少挨打',
              '只看两个敌人 A、B：先打 A 更好 ⟺ `k_A·damage_B < k_B·damage_A`',
              '相邻交换像冒泡排序，所以直接按 `k/damage` 排序'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错点：击杀次数是上取整，`(h - 1) // power + 1`',
                 '`s` 是累计秒数，敌人在被击败的那一秒仍然出手',
                 '用 `k/d` 浮点比较在本题值域安全；值域到 1e9 时改用 `cmp_to_key` 交叉相乘（写法二）',
                 '同类题：1665、2136'],
    ),
)
