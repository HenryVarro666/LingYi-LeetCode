CONFIG = dict(
    num=2262, title='字符串的总引力', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='f[i] = 以 s[i] 结尾的子串引力和',
    tags=['灵神题单', '动态规划', '难度分 2033'],
    code='''
class Solution(object):
    def appealSum(self, s):

        last_pos = {s[0] : 0}
        now = 1
        res = 1
        for index in range(1, len(s)):
            """
            if s[index] in last_pos:
                now += index - last_pos[s[index]]
            else:
                now += index + 1
            """

            now += index - last_pos.get(s[index], -1)
            res += now
            last_pos[s[index]] = index

        return res
''',
    call='Solution().appealSum("abbca")',
    skip=['"""'],
    expect=28,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前 index，粉 = 上次出现的同字符 p）', h=190, cell=90,
             pointers={'index': 'blue'},
             color=lambda S, k, v: ('blue' if k == S.get('index') else
                                    'pink' if 'index' in S and S['index'] < len(S['s']) and S['last_pos'].get(S['s'][S['index']], -1) == k and k != S['index'] and S.get('_line') in (11, 12) else None),
             dim=lambda S, k, v: 'index' in S and k > S['index']),
        dict(type='text', size=26, h=70, fn=lambda S: (
            f"`f[{S['index']}]` = `now` = {S['now']}，累计 `res` = {S['res']}" if 'index' in S else
            '`now` = f[i]：以 `s[i]` 结尾的所有子串的引力之和')),
        dict(type='map', var='last_pos', label='last_pos：字符最后一次出现的下标', h=170, fmt=lambda k, v: f'{k}:{v}'),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'yellow'), ('res', 'res', 'green')],
    captions={
        'last_pos = {': '`f[0]`：只有一个字符，引力 1；哈希表记下 `{s[0]}` 在 0',
        'now += index': lambda S, B, r: (
            f"`s[{S.index}] = {S.s[S.index]}` 之前出现过，最后在 `p = {S.last_pos[S.s[S.index]]}`：起点在 0..p 的子串得不到新引力，`f[i] = f[i-1] + {S.index} - {S.last_pos[S.s[S.index]]}` = =={S.now}==" if S.s[S.index] in S.last_pos else
            f"`s[{S.index}] = {S.s[S.index]}` 之前没出现过（p 当作 -1）：`{S.index + 1}` 个子串都多 1 点引力，`f[i] = f[i-1] + {S.index + 1}` = =={S.now}=="),
        'res += now': '`f[{index}]` 累加进答案：`res` = =={res}==',
        'last_pos[s[index]] = index': '更新哈希表：`{s[index]}` 最后一次出现在 `{index}`',
        'return res': '所有 `f[i]` 之和 = =={ret}==',
    },
    cards=dict(
        one_liner='f[i] 在 f[i-1] 基础上加 i - p，p 是上次出现的位置',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['字符串的==引力==是不同字符的个数，求所有子串引力之和',
                 '`|s|` 可达 10^5，不能枚举子串',
                 '示例：`s = "abbca"` → `28`'],
        quote='一般O(n)的状态有两种经典的状态表示法：f[i]表示前i个字符形成的子串如何如何；f[i]表示以s[i]结尾的所有子串如何如何。在这里使用第二种状态表示是比较合适的。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i]` 是在所有以 `s[i-1]` 结尾的子串后面加 `s[i]`，再加单独的 `s[i]`',
              '理想情况 `s[i]` 没出现过：`f[i] = f[i-1] + i + 1`',
              '若上次出现在 `p`，起点在 0..p 的子串已有它：`f[i] = f[i-1] + i - p`'],
        summary=['时间 `O(n)`，空间 `O(26)`：`f` 只依赖上一轮，用变量 `now` 滚动',
                 '易错：没出现过时 `p = -1`，所以 `get(c, -1)` 一个式子覆盖两种情况',
                 '初始 `now = res = 1` 对应 `f[0]`，循环从 1 开始',
                 '代码里三引号块是作者留下的等价写法注释（不执行）'],
    ),
)
