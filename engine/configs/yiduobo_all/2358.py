CONFIG = dict(
    num=2358, title='分组的最大数量', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='人数 1、2、3… 递增 · 枚举组数',
    tags=['灵神题单', '贪心与思维', '难度分 1503'],
    code='''
class Solution(object):
    def maximumGroups(self, grades):
        
        res = 1
        while res * (res + 1) // 2 <= len(grades):
            res += 1
        
        return res - 1
''',
    call='Solution().maximumGroups([10,6,12,7,3,5])',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"分 `{S['res']}` 组至少要 `{S['res']} × ({S['res']}+1) / 2` = =={S['res'] * (S['res'] + 1) // 2}== 人，现有 `{len(S['grades'])}` 人" if 'res' in S else ''), size=28),
        dict(type='array', var='grades', h=260,
             color=lambda S, i, v: 'green' if 'res' in S and i < S['res'] * (S['res'] + 1) // 2 and S['_line'] in (5, 6) else None),
    ],
    watch=[('res', 'res', 'green'), ('res*(res+1)//2', 'res * (res+1) // 2', 'blue'), ('len(grades)', 'len(grades)', 'pink')],
    captions={
        'res = 1': '先假设能分 1 组',
        'while res': lambda S, B, r: (f'`{S.res} × {S.res + 1} // 2 = {S.res * (S.res + 1) // 2} <= {len(S.grades)}`：人数够分 `{S.res}` 组 → 试试更多' if S.res * (S.res + 1) // 2 <= len(S.grades) else f'`{S.res * (S.res + 1) // 2} > {len(S.grades)}`：人数不够分 `{S.res}` 组 → ==停止=='),
        'res += 1': '`res` → {res}：再试试多分一组',
        'return res - 1': '循环停在第一个分不了的 `{res}`，所以答案是 `{res} - 1` = =={res - 1}==',
    },
    cards=dict(
        one_liner='按 1、2、3… 个人分组，只看总人数够不够',
        complexity='时间 `O(√n)`，空间 `O(1)`',
        problem=['给正整数数组 `grades`，分成有序的若干组',
                 '后一组的人数、总成绩都要比前一组大，求最多分几组',
                 '示例：`[10,6,12,7,3,5]` → `3`'],
        quote='为了尽可能多地分组，在分组人数上的最优做法就是按1、2、3、...，这种形式类推上去',
        quote_src='—— yiduobo 题解原文',
        idea=['总分要求其实不用管：按分数从低到高依次填进各组',
              '后一组每个人都不低于前一组，还多一个人，总分必然更大',
              '分 `k` 组至少要 `(1 + k) * k / 2` 个人，从 1 往上枚举到不够为止'],
        summary=['时间 `O(√n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '易错点：循环退出时 `res` 是第一个不行的组数，要返回 `res - 1`',
                 '数值本身不影响答案，只有人数 `n` 有用'],
    ),
)
