def _order(S):
    return sorted(zip(S['damage'], S['times']), key=lambda d: (d[1] * 1.0 / d[0]))


def _cur(S):
    if 'd' in S and 't' in S and 'times' in S:
        o = _order(S)
        return o.index((S['d'], S['t'])) if (S['d'], S['t']) in o else None
    return None


def _txt(S):
    if 'times' not in S:
        return '先算每个敌人要打几次（times），再决定先后顺序'
    if 's' not in S:
        return '`times[i]` = 击杀第 i 个敌人需要的秒数'
    if _cur(S) is None:
        return f'敌人处理完毕，总伤害 `res = {S["res"]}`'
    return f'此刻存活敌人总输出 `s = {S["s"]}`，击杀这个敌人要 `t = {S["t"]}` 秒'


CONFIG = dict(
    num=3273, title='对 Bob 造成的最少伤害', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='按 t/d 排序 · 维护存活总输出',
    tags=['灵神题单', '贪心与思维', '难度分 2013'],
    code='''
class Solution(object):
    def minDamage(self, power, damage, health):

        times = [(h - 1) // power + 1 for h in health]

        s = sum(damage)
        res = 0
        for d, t in sorted(zip(damage, times), key=lambda d:(d[1] * 1.0 / d[0])):
            res += s * t
            s -= d
        
        return res
''',
    call='Solution().minDamage(4, [1,2,3,4], [4,5,6,8])',
    expect=39,
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='array', var='times', cell=110, h=200, label='times（击杀所需秒数）'),
        dict(type='array', var='sorted(zip(damage, times), key=lambda d:(d[1] * 1.0 / d[0]))', cell=130, h=230,
             label='按 t/d 排好的 (damage, times)',
             color=lambda S, i, v: 'yellow' if _cur(S) == i else None,
             dim=lambda S, i, v: _cur(S) is not None and i < _cur(S)),
    ],
    watch=[('s', 's', 'blue'), ('res', 'res', 'green')],
    captions={
        'times = [': '`times[i] = (health[i] - 1) // power + 1`：击杀第 i 个敌人要的秒数 = {times}',
        's = sum(damage)': '`s` = 所有存活敌人每秒总输出，开始时全部存活：`{s}`',
        'res = 0': '`res` 累计 Bob 受到的伤害',
        'for d, t': '按 `t/d` 从小到大取下一个敌人：输出 `d = {d}`，击杀用时 `t = {t}`',
        'res += s * t': '击杀它的 `{t}` 秒里，所有存活敌人都在输出：`{s} × {t} = {s * t}` → `res = {res}`',
        's -= d': '它死了，存活总输出减去 `{d}` → `s = {s}`',
        'return res': '最少总伤害：`{res}`',
    },
    cards=dict(
        one_liner='先杀血少的还是输出高的？比 t/d，小的先杀',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['敌人活着时每秒造成 damage，之后 Bob 还击一个敌人，血量减 power',
                 '求杀光所有敌人前受到的最少伤害',
                 '示例：`power=4, damage=[1,2,3,4], health=[4,5,6,8]` → `39`'],
        quote='首先，根据伤其十指不如断其一指的说法，应该集中火力一个个击杀，而不应该轮流打每个敌人。',
        quote_src='—— yiduobo 题解原文',
        idea=['先算出击杀每个敌人所需时间 `times`',
              '两个敌人先杀谁：展开两种总伤害，约掉相同项，剩下比 `t1·d2` 与 `t2·d1`',
              '移项成 `t/d`，小的先杀；用 `s` 记存活总输出，击杀时 `res += s * t`，再 `s -= d`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错点：`s` 初始是全部伤害之和，杀一个减一个；击杀时间要上取整',
                 '原文已是 Python 3 可运行写法（`//`、`zip`、`sorted`），未做修改',
                 '对比灵神：灵神用前缀秒数 `s` 乘当前 damage；yiduobo 用「剩余存活输出」乘用时，结果相同'],
    ),
)
