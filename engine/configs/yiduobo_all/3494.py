def _t(S):
    if 't' not in S:
        return '`f[i]`：第 i 名巫师加工完==当前这瓶==药水的时间'
    if S['_line'] in (9, 10, 11, 12):
        return f"药水 `ma = {S['ma']}`：正序算最早完工时间，卡着上一瓶的 `f[index]` 取 max，当前 `t` = =={S['t']}=="
    return f"药水 `ma = {S['ma']}`：最后一名巫师完工 `f[-1]` = =={S['f'][-1]}==，向前倒推，保证药水不停顿"


CONFIG = dict(
    num=3494, title='酿造药水需要的最少总时间', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='先正推最早完工，再倒推',
    tags=['动态规划', '数学算法', '难度分 2042'],
    code='''
class Solution:
    def minTime(self, skill, mana):

        n = len(skill)
        f = [skill[0] * mana[0]]
        for index in range(1, n):
            f.append(f[-1] + skill[index] * mana[0])

        for ma in mana[1:]:
            t = f[0] + skill[0] * ma
            for index in range(1, n):
                t = max(t, f[index]) + skill[index] * ma

            f[-1] = t
            for index in range(n - 2, -1, -1):
                f[index] = f[index + 1] - skill[index + 1] * ma

        return f[-1]
''',
    call='Solution().minTime([1,5,2,4], [5,1,4])',
    expect=102,
    views=[
        dict(type='array', var='skill', label='skill', h=170, cell=90, pointers={'index': 'pink'}),
        dict(type='array', var='f', label='f（每名巫师加工完当前药水的时间）', h=170, cell=90, pointers={'index': 'pink'}),
        dict(type='array', var='mana', label='mana', h=170, cell=90,
             color=lambda S, i, v: 'blue' if S.get('ma') == v and i == S['mana'].index(v) else None),
        dict(type='text', fn=_t, size=26, h=70),
    ],
    watch=[('ma', 'ma', 'blue'), ('t', 't', 'yellow'), 'index'],
    skip=['n = len', 'for index in range', 'for ma in mana'],
    captions={
        'f = [skill[0]': '第一瓶药水最简单：从时间 0 开始，巫师依次加工。`f[0]` = {f[0]}',
        'f.append': '`f[{index}]` = 前一名完工 + `skill[{index}] × mana[0]` = =={f[index]}==',
        't = f[0] + skill[0] * ma': '后面的药水：先正推「最早完工时间」。第 0 名巫师做完上一瓶（`f[0]` = {f[0]}）才能开始，完工 `t` = =={t}==',
        't = max(t, f[index])': '`max({B.t}, f[{index}]={f[index]})` + `{skill[index]}×{ma}`：药水到了还得等巫师做完上一瓶 → `t` = =={t}==',
        'f[-1] = t': '最后一名巫师的完工时间就是 `t` = =={t}==。人可以等药水，药水不能等人，所以它定下了整瓶的节奏',
        'f[index] = f[index + 1]': '倒推：`f[{index}] = f[{index+1}] − skill[{index+1}]×{ma}` = =={f[index]}==，药水到下一名巫师手里立刻开工',
        'return f[-1]': '最后一名巫师做完最后一瓶药水：=={ret}==',
    },
    cards=dict(
        one_liner='人可以等药水，药水不能等人：正推一遍，再倒推一遍',
        complexity='时间 `O(nm)`，空间 `O(n)`',
        problem=['`n` 个巫师依次加工 `m` 瓶药水，耗时 `skill[i] * mana[j]`',
                 '一个巫师做完，药水必须立刻交给下一个人',
                 '示例：`skill=[1,5,2,4]`，`mana=[5,1,4,2]` → `110`；本视频取前 3 瓶 → `102`'],
        quote='按照题目的描述，可以简单概括成人可以等药水，但是药水不能等人。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一瓶：从 0 开始，累加每名巫师的耗时即可',
              '后面每瓶：正序遍历，当前巫师不能早于自己上一瓶的完工 `f[index]`，得到最后一名巫师的最早完工时间',
              '最后一名巫师定下时间后，向前倒推：自己的完工 = 下一人完工 − 下一人耗时'],
        summary=['时间 `O(nm)`，空间 `O(n)`',
                 '不能只看后一名巫师的上一瓶完工时间，要看后面所有人，所以才要整趟正推取 max',
                 '倒推时用的是 `skill[index + 1] * ma`',
                 '对比灵神：思路相同，灵神用 `last > sum_t` 手写 max，yiduobo 直接用 `max`；原文无 Python 2 专有写法，未改动代码'],
    ),
)
