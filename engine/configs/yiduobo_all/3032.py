def _txt(S):
    if 'x' not in S:
        return '逐个检查 `[a, b]` 里的每个数：各位数字有没有重复'
    y = S.get('y')
    v = sorted(S.get('vis', []))
    st = '全部不同' if S.get('flag') else '出现重复'
    if y:
        return f"检查 `x = {S['x']}`：还剩 `y = {y}`，已见数字 {v}"
    return f"`x = {S['x']}` 的数字 {v} → =={st}==，目前累计 `res = {S['res']}`"


def _col(S, i, v):
    return 'green' if 'x' in S and v == S['x'] else None


CONFIG = dict(
    num=3032, title='统计各位数字都不同的数字个数 II', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='暴力枚举 · 集合判重',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def numberCount(self, a, b):

        res = 0
        for x in range(a, b + 1):
            y = x
            vis = set()
            flag = True
            while y:
                v = y % 10
                if v in vis:
                    flag = False
                    break
                vis.add(v)
                y //= 10
            
            if flag:
                res += 1
        
        return res
''',
    call='Solution().numberCount(9, 15)',
    expect=6,
    views=[
        dict(type='text', h=80, size=30, fn=_txt),
        dict(type='array', var=lambda S: list(range(S['a'], S['b'] + 1)) if 'a' in S else [], label='区间 [a, b]', cell=96, h=200,
             color=lambda S, i, v: ('green' if v == S['x'] else None) if 'x' in S else None),
        dict(type='set', var='vis', label='vis（这个数已经出现过的数字）', fmt=lambda x: str(x), h=170),
    ],
    watch=[('x', 'x', 'blue'), 'y', 'v', ('flag', 'flag', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计各位数字都不同的数的个数',
        'for x in range': '枚举区间里的每个数 `x = {x}`',
        'y = x': '拷贝一份 `y`，用来一位一位拆数字',
        'vis = set()': '`vis` 记录 `{x}` 已经见过的数字，每个数重新清空',
        'flag = True': '先假设 `{x}` 的各位都不同',
        'while y': lambda S, B, r: (f'`y = {S.y}` 还没拆完，继续取最低位' if S.y else f'`y = 0`，所有数位都看完且没有重复'),
        'v = y % 10': '取最低位 `v = {y_before} % 10 = {v}`'.replace('{y_before}', '{B.y}'),
        'if v in vis': lambda S, B, r: (f'`{S.v}` 已经在 `vis` 里 → ==数字重复==' if S.v in S.vis else f'`{S.v}` 不在 `vis` 里 → 还没重复'),
        'flag = False': '`{x}` 有重复数字，`flag = False`',
        'break': '已经不合法，不用再拆了，跳出循环',
        'vis.add(v)': '`{v}` 记进 `vis`',
        'y //= 10': '去掉最低位：`y` → {y}',
        'if flag': lambda S, B, r: (f'`{S.x}` 各位都不同 → 计数' if S.flag else f'`{S.x}` 有重复 → 不计数'),
        'res += 1': '`res` → =={res}==',
        'return res': '区间里一共有 `{res}` 个各位数字都不同的数',
    },
    cards=dict(
        one_liner='数据规模小，逐个数拆位、用集合判重',
        complexity='时间 `O((b−a)·log b)`，空间 `O(1)`',
        problem=['给出 `a` 和 `b`，统计 `[a, b]` 中各位数字都不同的整数个数',
                 '例如 `11` 的两位都是 1，不算；`12` 算',
                 '本视频：`a = 9, b = 15` → `6`（9、10、12、13、14、15）'],
        quote='看题设可以使用数位动态规划来处理，不过本题的数据规模非常小，直接暴力枚举就可以了。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举 `x`，用 `y % 10` 取最低位、`y //= 10` 去掉最低位',
              '每取一位就查 `vis`：已经有了就重复，`flag = False` 并 `break`',
              '原文还提到数学解：压线时缩小规模，不压线时用 `C(k, n) * n!` 计数'],
        summary=['时间 `O((b−a)·log b)`，空间 `O(1)`',
                 '原文为 Python 2 写法，`y /= 10` 已改为 `y //= 10`',
                 '`vis` 要在每个 `x` 开头重新创建，`flag` 同理',
                 '范围很大时才需要数位 DP 或组合数学'],
    ),
)
