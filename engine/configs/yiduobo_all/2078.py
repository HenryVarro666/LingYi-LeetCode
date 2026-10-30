COLORS = [4, 4, 4, 2, 4, 3, 4, 4]


def _col(S, i, v):
    if i == 0:
        return 'blue'
    if 'second' in S and i == S['second']:
        return 'purple'
    return None


def _txt(S):
    if 'second' not in S:
        return '先找 `second`：最左边、颜色与房子 0 ==不同==的房子'
    c = S['colors']
    if 'index' in S and S['index'] > S['second']:
        i = S['index']
        if c[i] == c[0]:
            return f'房子 {i} 与房子 0 同色 → 只能配 `second`：距离 `{i} − {S["second"]} = {i - S["second"]}`'
        return f'房子 {i} 与房子 0 不同色 → 配房子 0：距离 `{i}`'
    return f'`second = {S["second"]}`：它右侧的房子，要么和房子 0 不同色，要么和 second 不同色'


CONFIG = dict(
    num=2078, title='两栋颜色不同且距离最远的房子', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='枚举右边房子 · 配 0 或 second',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def maxDistance(self, colors):

        for index in range(1, len(colors)):
            if colors[index] != colors[0]:
                res = index
                second = index
                break

        for index in range(second + 1, len(colors)):
            if colors[index] == colors[0]:
                res = max(res, index - second)
            else:
                res = max(res, index)
        
        return res
''',
    call=f'Solution().maxDistance({COLORS})',
    expect=5,
    views=[
        dict(type='array', var='colors', label='colors（蓝 = 房子 0，紫 = second）', pointers={'index': 'pink'},
             color=_col, cell=96, h=300),
        dict(type='text', fn=_txt, size=29, h=110),
    ],
    watch=[('index', 'index', 'pink'), ('second', 'second', 'purple'), ('res', 'res', 'green')],
    captions={
        'for index in range(1,': lambda S, B, ret: f'从左往右找第一栋与房子 0 颜色不同的房子：`index = {S.index}`',
        'if colors[index] != colors[0]': lambda S, B, ret: (f'`colors[{S.index}] = {S.colors[S.index]} ≠ colors[0] = {S.colors[0]}`：找到了'
                                                             if S.colors[S.index] != S.colors[0]
                                                             else f'`colors[{S.index}] = {S.colors[S.index]}` 与房子 0 同色，继续'),
        'res = index': '房子 0 和它组成第一对候选：`res = {res}`',
        'second = index': '记下 `second = {second}`：==下标最小==且颜色与房子 0 不同',
        'break': '找到就停',
        'for index in range(second': lambda S, B, ret: (f'枚举右边那栋 `index = {S.index}`（second 右侧）'
                                                         if 'index' not in B or S.index != B.index or B.index == S.second else '枚举结束'),
        'if colors[index] == colors[0]': lambda S, B, ret: (f'`colors[{S.index}] = {S.colors[S.index]}` 与房子 0 ==同色== → 最远只能配 second'
                                                            if S.colors[S.index] == S.colors[0]
                                                            else f'`colors[{S.index}] = {S.colors[S.index]}` 与房子 0 不同色 → 直接配最左的房子 0'),
        'res = max(res, index - second)': lambda S, B, ret: f'`max({B.res}, {S.index} − {S.second})` → `res = {S.res}`',
        'res = max(res, index)': lambda S, B, ret: f'`max({B.res}, {S.index})` → `res = {S.res}`',
        'return res': '最大距离 =={ret}==',
    },
    cards=dict(
        one_liner='枚举右边那栋：要么配房子 0，要么配 second',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`colors[i]` 是第 i 栋房子的颜色，求两栋==颜色不同==的房子的最大距离',
                 '示例：`[1,1,1,6,1,1,1]` → `3`；`[1,8,3,8,3]` → `4`',
                 '本视频：`[4,4,4,2,4,3,4,4]` → `5`'],
        quote='得到second后，对于second右侧的所有房子，其颜色==要么与下标为0的房子不同，要么与下标为second的房子不同==，换言之，要么是用index来更新答案，要么是用index - second来更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['暴力 `O(n^2)` 枚举每一对也能过；更好的是枚举右边那栋，找离它最远的左边房子',
              '最远且颜色不同的左边房子：不是房子 0，就是 `second`（最左的非同色房子）',
              '一趟扫描：同色配 second，不同色配 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`second` 前面的房子都和房子 0 同色，不会是更优的左端',
                 '`res`、`second` 在第一个循环里赋值，靠题目保证一定存在',
                 '原文为 Python 2 风格写法，代码可直接在 Python 3 运行，未作改动',
                 '对比灵神：灵神从两端分别找最近的非同色房子，取 `max(r, n−1−l)`'],
    ),
)
