CONFIG = dict(
    num=1881, title='插入后的最大值', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='分正负讨论 · 严格比较找插入点',
    tags=['灵神题单', '贪心与思维', '难度分 1381'],
    code='''
class Solution(object):
    def maxValue(self, n, x):

        if n[0] == '-':
            for index in range(1, len(n)):
                if int(n[index]) > x:
                    return n[:index] + str(x) + n[index:]
        else:
            for index in range(len(n)):
                if int(n[index]) < x:
                    return n[:index] + str(x) + n[index:]
            
        return n + str(x)
''',
    call='Solution().maxValue("-135792", 6)',
    expect="-1356792",
    views=[
        dict(type='text', fn=lambda S: (f"`n[{S['index']}] = {S['n'][S['index']]}` 对比 `x = {S['x']}`" if 'index' in S and S['index'] < len(S['n']) else f"在 `n = {S['n']}` 里插入数字 `{S['x']}`"), size=28),
        dict(type='string', var='n', pointers={'index': 'pink'}, h=260,
             color=lambda S, i, v: 'yellow' if 'index' in S and i == S['index'] and S['_line'] in (7, 8, 11, 12) else None),
    ],
    watch=['x', ('index', 'index', 'pink')],
    captions={
        'if n[0] ==': lambda S, B, r: ('`n[0]` 是负号 → ==负数==：高位要放更小的数' if S.n[0] == '-' else '`n[0]` 不是负号 → ==正数==：高位要放更大的数'),
        'for index in range(1': lambda S, B, r: ('负数跳过负号，从下标 `1` 开始往后看' if S.index == 1 else '看下一位：`index = {}`'.format(S.index)),
        'for index in range(len': lambda S, B, r: ('正数从最高位开始往后看' if S.index == 0 else '看下一位：`index = {}`'.format(S.index)),
        'if int(n[index]) > x': lambda S, B, r: (f'`{S.n[S.index]} > {S.x}`：这一位比 `x` 大，==x 放在它前面更小，整体更大==' if int(S.n[S.index]) > S.x else f'`{S.n[S.index]} > {S.x}` 不成立：当前位不比 x 大，继续往后'),
        'if int(n[index]) < x': lambda S, B, r: (f'`{S.n[S.index]} < {S.x}`：这一位比 `x` 小，==x 放在它前面更大，整体更大==' if int(S.n[S.index]) < S.x else f'`{S.n[S.index]} < {S.x}` 不成立：当前位不比 x 小，继续往后'),
        'return n[:index]': '在下标 `{index}` 前插入 `{x}` → =={ret}==',
        'return n + str(x)': '没有找到合适位置：`x` 放在末尾 → =={ret}==',
    },
    cards=dict(
        one_liner='正负分开看：正数放大的在高位，负数放小的在高位',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `n` 表示大整数，可能为负',
                 '在任意位置（不能在负号左边）插入数字 `x`，使数值最大',
                 '示例：`n = "-13", x = 2` → `"-123"`'],
        quote='在这里必须是严格的大于而不是大于等于，举个例子很容易就能说明。对于231而言，如果要插入一个2，那么插入在1的前方可以得到2321',
        quote_src='—— yiduobo 题解原文',
        idea=['正数：从高位往后找第一个比 `x` 小的数字，插在它前面',
              '负数：从高位往后找第一个比 `x` 大的数字，插在它前面',
              '相等时不插：插在后面才不会把更大的数挤到后面'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '必须是严格比较：相等就继续往后看',
                 '整个循环都没触发时，`x` 放到最后（`return n + str(x)`）',
                 '负数的循环从 1 开始，避开负号'],
    ),
)
