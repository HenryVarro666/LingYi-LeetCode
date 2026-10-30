STRS = ['ace', 'adb', 'bca', 'bba']


def _col(S, i, j, v):
    if 'i' not in S:
        return None
    if j == S['i']:
        if 'j' in S and S['_line'] in (14, 15, 16, 22, 23) and i in (S['j'], S['j'] + 1):
            return 'yellow'
        return 'blue'
    return None


def _txt(S):
    if 'small' not in S:
        return ''
    s = S['small']
    done = [f'{k}' for k, v in enumerate(s) if v]
    return f"已确定 `strs[j] < strs[j+1]` 的对：{'、'.join(done) if done else '暂无'}　　已删 =={S.get('res', 0)}== 列"


CONFIG = dict(
    num=955, title='删列造序 II', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='small 数组记录已分出大小的相邻行',
    tags=['灵神题单', '贪心与思维', '难度分 1876'],
    code='''
class Solution(object):
    def minDeletionSize(self, strs):

        n = len(strs)
        l = len(strs[0])
        small = [False] * (n - 1)
        
        res = 0
        for i in range(l):
            flag = False
            for j in range(n - 1):
                if small[j]:
                    continue
                if strs[j][i] > strs[j + 1][i]:
                    flag = True
                    break
            
            if flag:
                res += 1
            else:
                for j in range(n - 1):
                    if strs[j][i] < strs[j + 1][i]:
                        small[j] = True
        
        return res
''',
    call=f'Solution().minDeletionSize({STRS})',
    expect=2,
    views=[
        dict(type='text', fn=_txt),
        dict(type='table', var='strs', label='strs（蓝 = 当前列 i，黄 = 正在比较的两个字母）', h=300, cell=64,
             rows=lambda S: list(range(len(S['strs']))), cols=lambda S: list(range(len(S['strs'][0]))),
             color=_col),
        dict(type='array', var='small', label='small[j] = True：strs[j] 与 strs[j+1] 已确定前者更小', h=170,
             pointers={'j': 'blue'}, color=lambda S, i, v: 'green' if v else None),
    ],
    watch=['i', 'j', 'flag', ('res', 'res', 'green')],
    captions={
        'small = [False]': '`small[j]`：第 `j`、`j+1` 行是否已经确定 ==前者更小==（初始都未确定）',
        'res = 0': '`res` 统计删除的列数',
        'flag = False': '`flag`：这一列是否必须删除',
        'if small[j]': lambda S, B, r: (f'`small[{S.j}]` 已经为真 → 这两行以后无论怎样都满足，跳过' if S.small[S.j] else f'`small[{S.j}]` 还是假 → 这两行此前保留的列完全一致，要比这一列'),
        'continue': '跳过这一对',
        'if strs[j][i] >': lambda S, B, r: (f'比较 `{S.strs[S.j][S.i]}` 与 `{S.strs[S.j+1][S.i]}` → ' + ('前者更大：这一列==必须删==' if S.strs[S.j][S.i] > S.strs[S.j+1][S.i] else '没有逆序')),
        'flag = True': '发现逆序，`flag = True`，不用再看其它行',
        'res += 1': '这一列删除：`res = {res}`（`small` 不变）',
        'if strs[j][i] <': lambda S, B, r: (f'保留这一列：`{S.strs[S.j][S.i]}` ' + ('< ' if S.strs[S.j][S.i] < S.strs[S.j+1][S.i] else '不小于 ') + f'`{S.strs[S.j+1][S.i]}`' +
                                           (' → 这对大小已定' if S.strs[S.j][S.i] < S.strs[S.j+1][S.i] else ' → 相等，仍需看后面的列')),
        'small[j] = True': '`small[{j}] = True`：以后不必再比这对',
        'return res': '一共删 `{ret}` 列',
    },
    cards=dict(
        one_liner='用 small 标出“已经分出大小”的相邻行，之后不再比较',
        complexity='时间 `O(n * l)`，空间 `O(n)`',
        problem=['`n` 个等长字符串，删掉若干列，使剩下的行按字典序不降',
                 '求最少删几列',
                 f'本视频：`{STRS}` → `2`'],
        quote='于是我们可以使用一个数组small来记录当前这个确定的大小情况，当某一时刻small[j]为true时，说明之后的列我们无需考察第j行以及第j + 1行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['朴素做法：每列都拼出完整字符串再比，`O(n·l²)`',
              '`small[j]` 为假时，两行保留下来的列一定完全相同，只比当前列的字母',
              '这一列保留后，严格变小的那些对就标记为真'],
        summary=['时间 `O(n * l)`，空间 `O(n)`',
                 '易错点：`small[j]` 为真才能跳过；`<=` 并不能标记（相等还要看后面）',
                 '删除的列不更新 `small`',
                 '原文为 Python 2 写法，代码无需改动',
                 '对比灵神：灵神用 `check_list` 只保留还要比的对，这里用布尔数组跳过'],
    ),
)
