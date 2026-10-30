ARR = [2, -3, 4, -1, 5]


def _ix(S):
    return ARR.index(S['num']) if 'num' in S and S['num'] in ARR else None


def _text(S):
    if 'g' not in S:
        return '`f`：以当前数结尾、==没删==；`g`：以当前数结尾、==删过一次==（可删当前数）'
    return f'`f` = =={S["f"]}==（没删）　`g` = =={S["g"]}==（删过）　`res` = =={S["res"]}=='


def _cap_g(S, B, ret):
    keep, dele = B.g + S.num, B.f
    if keep >= dele:
        return f'`g = max({B.g} + {S.num}, {B.f})` = =={S.g}==：保留 `{S.num}`，接在旧 `g` 后'
    return f'`g = max({keep}, {B.f})` = =={S.g}==：删掉 `{S.num}`，取上一轮没删的 `f`（==必须先更新 g==）'


def _cap_f(S, B, ret):
    if B.f > 0:
        return f'旧 `f = {B.f}` > 0，保留并接上 `{S.num}` → `f = {S.f}`'
    return f'旧 `f = {B.f}` 不大于 0，舍去，只留 `{S.num}` → `f = {S.f}`'


CONFIG = dict(
    num=1186, title='删除一次得到子数组最大和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='最大子段和进阶 · f / g 滚动',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1799'],
    code='''
class Solution(object):
    def maximumSum(self, arr):

        f = res = arr[0]
        g = 0
        for num in arr[1:]:
            g = max(g + num, f)
            f = max(f, 0) + num
            res = max(res, f, g)
        
        return res
''',
    call=f'Solution().maximumSum({ARR})',
    expect=10,
    views=[
        dict(type='text', fn=_text, size=26, h=70),
        dict(type='array', var='arr', label='arr（蓝 = 当前 num）', cell=96, h=260,
             pointers={_ix: 'blue'}, pointer_labels={_ix: 'num'},
             color=lambda S, i, v: 'blue' if _ix(S) == i else None),
    ],
    watch=[('f', 'f', 'blue'), ('g', 'g', 'pink'), ('res', 'res', 'green'), ('num', 'num', 'yellow')],
    captions={
        'f = res = arr[0]': '第一个数：`f = res = {f}`（没删过的最大子段和）',
        'g = 0': '`g = 0`：还没有「删过」的方案',
        'g = max': _cap_g,
        'f = max': _cap_f,
        'res = max': '`res = max({B.res}, f={f}, g={g})` = =={res}==',
        'return res': '一趟遍历取到的最大值 = =={ret}==',
    },
    cards=dict(
        one_liner='f 表示没删过，g 表示删过一次，滚动更新',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['在非空子数组里可以再删掉一个数，求剩余元素和的最大值',
                 '示例：`[1,-2,0,3]` → `4`',
                 '本视频：`[2,-3,4,-1,5]` → `10`'],
        quote='令f[i]表示以arr[i]结尾，且没有删除过数字的最大子段和是多少，令g[i]表示以arr[i]结尾，删除过一次数字的最大子段和是多少，这里的删除也可以是删除掉arr[i]本身。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i] = max(f[i-1], 0) + arr[i]`：前面为正就保留，否则舍去',
              '`g[i] = max(g[i-1] + arr[i], f[i-1])`：保留 `arr[i]`，或把它删掉',
              '只依赖上一轮，==先更新 g 再更新 f==，省掉一维'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`g` 要先于 `f` 更新，否则会读到新的 `f`',
                 '从 `arr[1:]` 开始遍历，`f = res = arr[0]` 保证非空；`g` 初值 0 会被 `f` 覆盖',
                 '对比灵神：灵神用 `-inf` 表示非法状态，这里靠初始值和遍历起点避开'],
    ),
)
