_I = lambda S: S['_inner'].get('index')


def _if(S, B, ret):
    idx, ch, last, used, cl = S['index'], S['char'], B.last, S['used'], S['char_list']
    if used[idx]:
        return f'`char_list[{idx}] = {ch}` ==已被用过== → 跳过'
    if ch == last:
        return f'`{ch}` 和本轮上一个选的 `{last}` ==相同== → 跳过，否则会得到重复序列'
    return f'`{ch}` 没用过，且本轮还没选过 `{ch}` → 选它'


CONFIG = dict(
    num=1079, title='活字印刷', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='排序去重 + 暴力 DFS',
    tags=['难度分 1741'],
    code='''
class Solution(object):
    def numTilePossibilities(self, tiles):

        self.res = 0
        char_list = sorted(list(tiles))
        used = [False] * len(char_list)
        self.dfs(0, char_list, used)
        return self.res - 1

    def dfs(self, level, char_list, used):
        self.res += 1
        if level == len(char_list):
            return

        last = ''
        for index, char in enumerate(char_list):
            if char != last and not used[index]:
                used[index] = True
                last = char
                self.dfs(level + 1, char_list, used)
                used[index] = False
''',
    call='Solution().numTilePossibilities("AAB")',
    expect=8,
    max_steps=110,
    skip=['last = ', 'used[index] = True', 'self.res += 1'],
    views=[
        dict(type='array', var='char_list', label='char_list（排序后；绿 = 已选进当前序列）', cell=80, h=200,
             pointers={'index': 'pink'},
             color=lambda S, i, v: 'green' if S['used'][i] else None),
        dict(type='calls', h=400, hide=('char_list', 'used', 'self')),
    ],
    watch=[('level', 'level', 'blue'), ('index', 'index', 'pink'), ('last', 'last', 'yellow'), ('res', 'self.res', 'green')],
    captions={
        'self.res = 0': '`res` 统计所有序列（先把空序列也算进去，最后再减 1）',
        'sorted(list(tiles))': '==先排序==：相同字母挨在一起，才能靠「和前一个相同就跳过」去重 → `{char_list}`',
        'used = [False]': '`used[i]` 标记第 `i` 个字模是否已被当前序列用掉',
        'self.dfs(0': '从长度 0 的序列（空序列）出发开始 dfs',
        'return self.res - 1': '`res` 把空序列也数了一次，所以减 1 → =={ret}==',
        'if level == len': lambda S, B, r: (f'进入新一层，当前序列本身是一个新序列：`res` → =={S.self.res}==；`level = {S.level}` 已用完所有字模 → 返回' if S.level == len(S.char_list)
                                            else f'进入新一层，当前序列本身是一个新序列：`res` → =={S.self.res}==；`level = {S.level}` < {len(S.char_list)}，继续选'),
        'for index, char': lambda S, B, r: ('枚举结束，这一层没有更多可选的了' if 'index' in B['_inner'] and B['_inner']['index'] == S['_inner'].get('index')
                                            else f"枚举字模：`index = {S['_inner']['index']}`，`char = {S['_inner']['char']}`"),
        'if char != last': _if,
        'used[index] = True': '选 `char_list[{index}] = {char}`，标记已用',
        'last = char': '记下这一轮选过 `{char}`，之后遇到相同字母就跳过',
        'self.dfs(level + 1': '选 `{B.char}` 作第 `{B.level + 1}` 个字母（标记已用，`last = {B.char}`），递归去选第 `{B.level + 2}` 个',
        'used[index] = False': '回溯：撤销选择，`used[{index}]` 恢复 False',
    },
    cards=dict(
        one_liner='排序后暴力 DFS：同一位置相同字母只选一次',
        complexity='时间 `O(n·n!)`，空间 `O(n)`（n ≤ 7）',
        problem=['`tiles` 是若干字母字模，每个只能用一次，求能印出的==非空==序列数',
                 '相同字母的字模不区分',
                 '示例：`"AAB"` → `8`（`A B AA AB BA AAB ABA BAA`）'],
        quote='tiles长度小于等于7，因此我选择的是直接暴力dfs。……为了避免重复，同一轮选择的tile不应该重复，因此可以先将tile排序，然后在枚举时若当前的tile[index]与tile[index - 1]一样，那么就跳过tile[index]。',
        quote_src='—— yiduobo 题解',
        idea=['每一层从没用过的字模里选一个，递归到最多 `len(tiles)` 层',
              '每进入一层，当前序列就是一个新序列，`res` 加 1',
              '排序后用 `last` 记录本层选过的字母，相同的跳过，避免重复序列'],
        summary=['最多 `n` 层，序列数最多 `O(n·n!)`；`n ≤ 7` 所以暴力够用',
                 '易错：要先排序；去重是在「同一层」里，不是全局',
                 '易错：`res` 含空序列，返回要 `- 1`',
                 '作者还提到可用母函数（组合数学）做'],
    ),
)
