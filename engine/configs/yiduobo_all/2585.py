CONFIG = dict(
    num=2585, title='获得分数的方法数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='背包 · 倒序枚举 · 减法代替取余',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1910'],
    code='''
class Solution(object):
    def waysToReachTarget(self, target, types):

        f = [0] * (target + 1)
        f[0] = 1
        mod = 10 ** 9 + 7
        for count, mark in types:
            for i in range(target, -1, -1):
                for j in range(1, count + 1):
                    if i >= j * mark:
                        f[i] += f[i - j * mark]
                        if f[i] >= mod:
                            f[i] -= mod
        
        return f[target]
''',
    call='Solution().waysToReachTarget(4, [[2,1],[2,2]])',
    expect=2,
    skip=['for i in range', 'for j in range', 'if f[i] >= mod'],
    max_steps=70,
    views=[
        dict(type='text', size=24, h=50, fn=lambda S: (
            f'当前题型：`{S["count"]}` 道，每道 `{S["mark"]}` 分' if 'count' in S else '`f[i]` = 前 k 类题恰好得 i 分的方案数')),
        dict(type='array', var='types', label='types = [道数, 每道分数]', h=190, cell=110,
             color=lambda S, k, v: 'blue' if S.get('count') is not None and v == [S['count'], S['mark']] else None),
        dict(type='array', var='f', label='f[i]（pink = 正在更新的 i，blue = 来源）', h=220, cell=80, pointers={'i': 'pink'},
             color=lambda S, k, v: ('blue' if S.get('i') is not None and S.get('j') is not None and S.get('mark')
                                    and k == S['i'] - S['j'] * S['mark'] and S.get('_line', 0) == 11 else None)),
    ],
    watch=[('count', 'count', 'cyan'), ('mark', 'mark', 'blue'), ('i', 'i', 'pink'), ('j', 'j', 'yellow')],
    captions={
        'f[0] = 1': '`f[0] = 1`：得 0 分有一种方式',
        'mod =': '`mod = 10^9+7`',
        'for count, mark in types': lambda S, B, r: ('所有题型都处理完了' if B.get('mark') == S.mark and B.get('count') == S.count and B.get('mark') is not None
                                                     else f'加入第 k 类题：`{S.count}` 道，每道 `{S.mark}` 分'),
        'if i >= j * mark': lambda S, B, r: (f'做 `{S.j}` 道 = `{S.j * S.mark}` 分，`i = {S.i}`：' + ('够用，可以加' if S.i >= S.j * S.mark else '超过 i 了，不能做')),
        'f[i] += f[i - j * mark]': '`f[{i}] += f[{i - j * mark}]`：做 `{j}` 道，剩 `{i - j * mark}` 分看上一轮 → =={f[i]}==',
        'f[i] -= mod': '超过 `mod` 就减去一次，代替取余',
        'return f[target]': '`f[target] = {ret}`',
    },
    cards=dict(
        one_liner='f 倒序更新，上一类题的结果不会被覆盖',
        complexity='时间 `O(target·S)`，空间 `O(target)`',
        problem=['每种题型有 `count` 道、每道 `mark` 分，同类题无法区分',
                 '恰好得到 `target` 分的方法数，对 `10^9+7` 取余',
                 '示例：`target=6, types=[[6,1],[3,2],[2,3]]` → `7`；视频用 `target=4, [[2,1],[2,2]]`'],
        quote='f[k][i] = f[k-1][i] + f[k-1][i-marks] + f[k-1][i-marks*2] + ... + f[k-1][i-marks*count]。由于f每一轮只与上一轮有关，因此可以通过倒序枚举i来省去k这一维。',
        quote_src='—— yiduobo 题解原文',
        idea=['先写二维：第 k 类题做 0 到 `count` 道，各加一项',
              '每一轮只依赖上一轮，所以压成一维',
              '`i` 倒序：`f[i - j*mark]` 还是上一轮的值，不会重复使用'],
        summary=['时间 `O(target·S)`，空间 `O(target)`',
                 '`i >= j * mark` 才能转移，否则下标为负',
                 '两个小于 mod 的数相加不会超过 2·mod，减一次就够，不必每次 `%`',
                 '原文即 Python 3 可运行写法，未作修改',
                 '对比灵神：灵神把 `j` 的上界算好再 `%=`；yiduobo 在循环里判断并减 mod'],
    ),
)
