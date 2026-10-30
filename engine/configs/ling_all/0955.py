STRS = ['ace', 'adb', 'bca', 'bba']


def _col(S, i, j, v):
    if 'j' not in S:
        return None
    jj = S['j']
    if j == jj:
        if 'i' in S and S['_line'] in (9, 10, 11, 12, 17, 18, 19, 20) and i in (S['i'], S['i'] + 1):
            return 'yellow'
        return 'blue'
    return None


def _txt(S):
    if 'check_list' not in S:
        return ''
    cl = S['check_list']
    pairs = '、'.join(f'`strs[{i}]` vs `strs[{i+1}]`' for i in cl)
    return f"还没分出大小的相邻对：{pairs if cl else '无（后面的列随便留）'}　　已删 =={S.get('ans', 0)}== 列"


CONFIG = dict(
    num=955, title='删列造序 II', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='列升序就保留 · 只比较仍相等的相邻对',
    tags=['灵神题单', '难度分 1876'],
    code='''
class Solution:
    def minDeletionSize(self, strs: List[str]) -> int:
        n, m = len(strs), len(strs[0])
        check_list = list(range(n - 1))

        ans = 0
        for j in range(m):
            for i in check_list:
                if strs[i][j] > strs[i + 1][j]:
                    # j 列不是升序，必须删
                    ans += 1
                    break
            else:
                # j 列是升序，不删更好
                new_size = 0
                for i in check_list:
                    if strs[i][j] == strs[i + 1][j]:
                        # 相邻字母相等，下一列 i 和 i+1 需要继续比大小
                        check_list[new_size] = i  # 原地覆盖
                        new_size += 1
                del check_list[new_size:]
        return ans
''',
    call=f'Solution().minDeletionSize({STRS})',
    expect=2,
    views=[
        dict(type='text', fn=_txt),
        dict(type='table', var='strs', label='strs（蓝 = 当前列 j，黄 = 正在比较的两个字母）', h=300, cell=64,
             rows=lambda S: list(range(len(S['strs']))), cols=lambda S: list(range(len(S['strs'][0]))),
             color=_col),
        dict(type='array', var='check_list', label='check_list（i 表示还要比较 strs[i] 与 strs[i+1]）', h=170,
             pointers={'i': 'blue'}),
    ],
    watch=['j', 'i', ('ans', 'ans', 'green'), 'new_size', ('check_list', 'check_list', 'cyan')],
    captions={
        'check_list = list': '一开始所有相邻对都要比：`check_list = {check_list}`',
        'if strs[i][j] >': lambda S, B, r: (f'比较 `{S.strs[S.i][S.j]}` 与 `{S.strs[S.i+1][S.j]}`（`strs[{S.i}]` 对 `strs[{S.i+1}]`）→ ' +
                                          ('前者更大，这对 ==逆序==' if S.strs[S.i][S.j] > S.strs[S.i+1][S.j] else '没有逆序')),
        'ans += 1': '这一列有逆序，不删就排不成字典序 → ==必须删==：`ans = {ans}`',
        'new_size = 0': '这一列升序，==保留==。重新整理 `check_list`：只留下字母相等的相邻对',
        'if strs[i][j] ==': lambda S, B, r: (f'`{S.strs[S.i][S.j]}` 与 `{S.strs[S.i+1][S.j]}` ' +
                                           ('相等 → 下一列还得比' if S.strs[S.i][S.j] == S.strs[S.i+1][S.j] else '已经 `<` → 大小已定，以后不用再比这对')),
        'check_list[new_size] = i': '原地覆盖：保留第 `{i}` 对，放到位置 `{B.new_size}`',
        'new_size += 1': '`new_size` → {new_size}',
        'del check_list': '截掉多余的尾部：`check_list = {check_list}`',
        'return ans': '一共删 `{ret}` 列',
    },
    cards=dict(
        one_liner='列升序就留着，留得越早，后面要比的对越少',
        complexity='时间 `O(nm)`，空间 `O(n)`',
        problem=['`n` 个等长字符串，删掉若干列，使剩下的 `strs[0] <= strs[1] <= ...` 字典序',
                 '求最少删几列',
                 f'本视频：`{STRS}` → `2`'],
        quote='当列已经是升序时，不删更好，后面需要比较的字母更少，更容易满足要求，最终删除的列更少。如果列不是升序，那么一定要删。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左到右贪心：这一列有逆序就删，升序就留',
              '留下后，字母严格变小的相邻对大小已定，不必再比',
              '只用 `check_list` 记录“前缀仍相等”的相邻对，原地覆盖删除'],
        summary=['时间 `O(nm)`，空间 `O(n)`；优化前的拼接写法是 `O(nm²)`',
                 '易错点：只有前面保留的列都相等的相邻对才需要比较当前列',
                 '`for ... else`：没有 `break` 才进入 else（该列升序）',
                 '灵神还给了优化前的写法：用 `a[i] += s[j]` 拼出保留的字符串再整体比较'],
    ),
)
