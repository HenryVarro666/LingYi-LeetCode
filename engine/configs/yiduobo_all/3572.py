def _lp(names, txt, end):
    def f(S, B, r):
        if all(n in B and B[n] == S[n] for n in names):
            return end
        return txt(S)
    return f


CONFIG = dict(
    num=3572, title='选择不同 X 值三元组使 Y 值之和最大', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='哈希表记最大 y · 手写维护前三大',
    tags=[],
    code='''
class Solution(object):
    def maxSumDistinctTriplet(self, x, y):
        
        value_dict = {}
        for x_v, y_v in zip(x, y):
            if x_v not in value_dict or value_dict[x_v] < y_v:
                value_dict[x_v] = y_v
        
        first, second, third = None, None, None
        for v in value_dict.values():
            if first is None or first < v:
                first, second, third = v, first, second
            elif second is None or second < v:
                second, third = v, second
            elif third is None or third < v:
                third = v
        
        if third is None:
            return -1
        
        return first + second + third
''',
    call='Solution().maxSumDistinctTriplet([1,2,1,3,2,4], [5,3,4,6,2,9])',
    expect=20,
    skip=['first, second, third = None'],
    views=[
        dict(type='array', var='x', label='x（蓝 = 当前这一对）', h=190, cell=80,
             color=lambda S, i, v: 'blue' if S.get('x_v') is not None and S['x'][i] == S['x_v'] and S['y'][i] == S['y_v'] else None),
        dict(type='array', var='y', label='y', h=170, cell=80,
             color=lambda S, i, v: 'blue' if S.get('x_v') is not None and S['x'][i] == S['x_v'] and S['y'][i] == S['y_v'] else None),
        dict(type='map', var='value_dict', label='value_dict（x 值 → 最大 y）', fmt=lambda k, v: f'x={k}: {v}', h=170, font=30),
        dict(type='text', h=110, size=32,
             fn=lambda S: f"前三大：`first = {S['first']}`，`second = {S['second']}`，`third = {S['third']}`" if 'first' in S else ''),
    ],
    watch=['x_v', 'y_v', 'v', ('first', 'first', 'green'), ('second', 'second', 'yellow'), ('third', 'third', 'cyan')],
    max_steps=80,
    captions={
        'value_dict = {}': '哈希表：每种 x 对应的最大 y',
        'for x_v, y_v in zip': _lp(['x_v', 'y_v'], lambda S: f'取一对：`x = {S.x_v}`，`y = {S.y_v}`', '所有下标都处理完，哈希表建好了'),
        'if x_v not in': lambda S, B, r: (f'`x = {S.x_v}` 第一次出现 → 直接记下' if S.x_v not in B.get('value_dict', {}) else (f'`{S.x_v}` 已有 `{S.value_dict[S.x_v]}`，比新的 `{S.y_v}` 小 → 更新' if S.value_dict[S.x_v] < S.y_v else f'`{S.x_v}` 已有 `{S.value_dict[S.x_v]}`，不比 `{S.y_v}` 小 → 保留')),
        'value_dict[x_v] = y_v': '`value_dict[{x_v}] = {y_v}`',
        'for v in value_dict': _lp(['v'], lambda S: f'现在从每种 x 的最大 y 里选最大的三个：看 `v = {S.v}`', '哈希表的值都看完了，前三大定下来'),
        'if first is None or': lambda S, B, r: ((f'`first` 还是空：`v = {S.v}` 成为最大' if S.first is None else f'`first = {S.first} < {S.v}`：`v` 成为新的最大，原来的往后顺延') if (S.first is None or S.first < S.v) else f'`{S.v}` 不比 `first = {S.first}` 大，看第二名'),
        'first, second, third = v': '顺延：`first = {first}`，`second = {second}`，`third = {third}`',
        'elif second is None or': lambda S, B, r: ((f'`second` 还是空：`v = {S.v}` 成为第二大' if S.second is None else f'`second = {S.second} < {S.v}`：`v` 成为第二大') if (S.second is None or S.second < S.v) else f'`{S.v}` 不比 `second = {S.second}` 大，看第三名'),
        'second, third = v': '`second = {second}`，`third = {third}`',
        'elif third is None or': lambda S, B, r: ((f'`third` 还是空：`v = {S.v}` 成为第三大' if S.third is None else f'`third = {S.third} < {S.v}`：`v` 成为第三大') if (S.third is None or S.third < S.v) else f'`{S.v}` 不比 `third = {S.third}` 大，丢弃'),
        'third = v': '`third = {third}`',
        'if third is None': lambda S, B, r: ('`third` 仍是 None：不足三种 x 值 → 返回 -1' if S.third is None else '`third` 有值：至少三种不同的 x 值'),
        'return first': '`first + second + third = {first} + {second} + {third}` = =={ret}==',
    },
    cards=dict(
        one_liner='先每种 x 留最大 y，再手动挑出最大的三个',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['选三个下标，对应的 `x` 两两不同，使 `y` 之和最大',
                 '不存在则返回 `-1`',
                 '本视频：`x=[1,2,1,3,2,4]`，`y=[5,3,4,6,2,9]` → `20`'],
        quote='若其被选择了，就应该选择对应的y最大的那个x。于是可以先一趟遍历，使用哈希表记录每种x对应的y的最大值。',
        quote_src='—— yiduobo 题解原文',
        idea=['选了某个 `x` 值，就该选它对应最大的 `y`',
              '一趟遍历建哈希表，把问题变成“从若干个数里选最大的三个”',
              '再遍历一次，用 `first/second/third` 三个变量维护前三大，新数插入时后面的顺延'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`first, second, third = v, first, second` 是顺延，右边用的都是旧值',
                 '`third is None` 说明不足三种 x，返回 `-1`',
                 '原文已是 Python 3 可运行写法，无需修改',
                 '对比灵神：灵神用 `nlargest(3, …)`，yiduobo 手写三个变量，免排序'],
    ),
)
