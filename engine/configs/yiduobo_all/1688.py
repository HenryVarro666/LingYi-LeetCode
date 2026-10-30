CONFIG = dict(
    num=1688, title='比赛中的配对次数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='脑筋急转弯 · 淘汰 n-1 支队伍',
    code='''
class Solution(object):
    def numberOfMatches(self, n):

        return n - 1
''',
    call='Solution().numberOfMatches(7)',
    expect=6,
    views=[
        dict(type='text', h=120, size=40, fn=lambda S: f"队伍数 `n = {S['n']}`" if 'n' in S else ''),
        dict(type='array', var=lambda S: ['淘汰'] * (S['n'] - 1) + ['冠军'], h=200, label='n 支队伍：n−1 支被淘汰，1 支夺冠', index=False,
             color=lambda S, i, v: 'green' if v == '冠军' else 'pink'),
        dict(type='text', h=120, size=38, fn=lambda S: f"每场淘汰 1 队 → 需要 `{S['n']} − 1` = =={S['n'] - 1}== 场"),
    ],
    watch=['n', ('场数', 'n - 1', 'green')],
    captions={
        'return n - 1': '每场比赛恰好淘汰 1 支队伍，只剩冠军就要淘汰 `{n} - 1` 支 → 共 =={ret}== 场',
    },
    cards=dict(
        one_liner='每场淘汰一支队伍，决出冠军要淘汰 n-1 支',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['比赛有 `n` 支队伍：偶数支两两配对，奇数支则一支轮空晋级',
                 '每一轮配对的场数相加，直到决出一支冠军，求总共比赛多少场',
                 '示例：`n = 7` → `6`（3 + 2 + 1）'],
        quote='由于一场比赛只会淘汰掉一只队伍，要从n支队伍中决出冠军，就需要淘汰掉n - 1只队伍，因此一共需要安排n - 1场比赛。',
        quote_src='—— yiduobo 题解原文',
        idea=['不用模拟每一轮：==一场比赛淘汰一支队伍==',
              '最后只剩 1 支，所以总共淘汰 `n - 1` 支',
              '场数 = 淘汰数 = `n - 1`'],
        before=[dict(heading='验证 n = 7', lines=['第 1 轮：7 队 → 3 场，晋级 4 队（含 1 支轮空）',
                                                  '第 2 轮：4 队 → 2 场，晋级 2 队',
                                                  '第 3 轮：2 队 → 1 场，决出冠军',
                                                  '`3 + 2 + 1 = 6 = 7 - 1`'])],
        after=[dict(heading='为什么不用模拟', lines=['模拟每一轮要处理奇偶，写起来麻烦', '换个角度数「淘汰」：每场恰好一个输家', '输家总数固定为 `n - 1`，一行代码搞定'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错点：不要被「奇数轮空」干扰，轮空的队伍没有被淘汰',
                 '模拟每一轮也能做，但答案恒等于 `n - 1`',
                 '这类题找「不变量」：每场固定淘汰一支'],
    ),
)
