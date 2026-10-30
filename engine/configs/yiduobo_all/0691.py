STK = ['ab', 'bc']
TGT = 'abbc'


def _st(S):
    f = S.get('f')
    if f is None:
        return '把 target 每个字母编码成一位：`target[i]` ↔ `2^i`，全集 = 所有位都是 1'
    n = len(S['target'])
    now = S['_inner'].get('now')
    if now is None:
        return '`f[status]`：拼出 status 里还没拼的字母，最少还要几张贴纸'
    left = ''.join(S['target'][i] for i in range(n) if now >> i & 1) or '空'
    return f'`now = {now:0{n}b}`：还需要拼 =={left}=='


def _cell(S, i, v):
    now = S['_inner'].get('now')
    tmp = S['_inner'].get('tmp')
    if now is not None and i == now:
        return 'yellow'
    if tmp is not None and i == tmp:
        return 'blue'
    return None


CONFIG = dict(
    num=691, title='贴纸拼词', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 记忆化 DFS',
    tags=['链表树与回溯'],
    code='''
class Solution(object):
    def minStickers(self, stickers, target):

        char_dict = {}
        stickers_list = []
        for index, sticker in enumerate(stickers):
            tmp = {}
            for char in sticker:
                tmp[char] = tmp.get(char, 0) + 1
            stickers_list.append(tmp.items())
            for char in tmp:
                if char not in char_dict:
                    char_dict[char] = []
                char_dict[char].append(index)

        target_dict = {}
        pos_dict = {}
        for index, char in enumerate(target):
            if char not in char_dict:
                return -1
            if char not in target_dict:
                pos_dict[char] = 0
                target_dict[char] = []
            target_dict[char].append(1 << index)

        f = [None] * (1 << len(target))
        f[0] = 0
        return self.dfs((1 << len(target)) - 1, f, pos_dict, target_dict, char_dict, stickers_list)

    def dfs(self, now, f, pos_dict, target_dict, char_dict, stickers_list):
        if f[now] is None:
            for char in pos_dict:
                if pos_dict[char] != len(target_dict[char]):
                    break

            stickers_index = char_dict[char]
            for index in stickers_index:
                tmp = now
                tmp_pos_dict = pos_dict.copy()
                for char, cnt in stickers_list[index]:
                    while char in target_dict and cnt > 0 and tmp_pos_dict[char] < len(target_dict[char]):
                        tmp -= target_dict[char][tmp_pos_dict[char]]
                        tmp_pos_dict[char] += 1
                        cnt -= 1
                f[tmp] = self.dfs(tmp, f, tmp_pos_dict, target_dict, char_dict, stickers_list)
                if f[now] is None or f[now] > f[tmp] + 1:
                    f[now] = f[tmp] + 1

        return f[now]
''',
    call=f'Solution().minStickers({STK}, {TGT!r})',
    expect=2,
    views=[
        dict(type='string', var='target', label='target', h=150, cell=90),
        dict(type='array', var='f', label='f[status]：拼出 status 里的字母最少要几张（None = 还没算；下标 = 二进制 status）', h=250, cell=84,
             color=_cell),
        dict(type='calls', h=200, hide=('f', 'pos_dict', 'target_dict', 'char_dict', 'stickers_list')),
        dict(type='text', fn=_st, size=26, h=90),
    ],
    watch=[('now', "_inner.get('now')", 'blue'), ('tmp', "_inner.get('tmp')", 'orange')],
    skip=['char_dict = {}', 'stickers_list = []', 'for index, sticker', 'tmp = {}', 'for char in sticker', 'tmp[char] = tmp.get',
          'if char not in char_dict:', 'char_dict[char] = []', 'for char in tmp', 'target_dict = {}', 'pos_dict = {}',
          'for index, char in enumerate(target)', 'if char not in char_dict:', 'if char not in target_dict', 'pos_dict[char] = 0',
          'target_dict[char] = []', 'for char in pos_dict', 'if pos_dict[char] !=', 'break', 'for index in stickers_index', 'tmp = now',
          'tmp_pos_dict = pos_dict.copy()', 'for char, cnt in stickers_list', 'while char in', 'tmp_pos_dict[char] += 1', 'cnt -= 1',
          'f[0] = 0'],
    captions={
        'stickers_list.append': '第 `{index}` 张贴纸 `{sticker}` 的字母计数记下：`{list(tmp.items())}`',
        'char_dict[char].append(index)': '`char_dict[{char!r}]`：含字母 {char!r} 的贴纸有 `{char_dict[char]}`',
        'target_dict[char].append': '`target[{index}] = {char!r}` 编码为 `1 << {index}` = `{1 << index}` → `target_dict[{char!r}] = {target_dict[char]}`',
        'f = [None]': '`f[status]` 先全是 `None`（还没算）；`status` 的第 i 位为 1 = `target[i]` 还没拼出',
        'return self.dfs': lambda S, B, r: (f'从全集 `{(1 << len(S.target)) - 1}`（所有字母都没拼）开始 `dfs`' if r is None else f'最少需要 `{r}` 张贴纸'),
        'if f[now] is None:': lambda S, B, r: (f'`f[{B.now}]` 还没算 → 往下算' if B.f[B.now] is None else f'`f[{B.now}] = {B.f[B.now]}` 已经算过 → ==直接用，不再重复搜索=='),
        'stickers_index = char_dict[char]': lambda S, B, r: (f'取一个还没拼完的字母 `{S.char!r}`：它必须被某张贴纸盖住，所以==只枚举含它的贴纸== `{S.stickers_index}`'),
        'tmp -= target_dict': '这张贴纸盖住 `{char!r}`：状态去掉对应的位 → `tmp = {tmp}`（剩 `{tmp:0{len(target)}b}`）',
        'f[tmp] = self.dfs': '递归求解贴完后的状态 `tmp`，贴纸 `{index}` 用了一张',
        'if f[now] is None or': lambda S, B, r: (f'`f[{S.now}] = f[{S.tmp}] + 1 = {S.f[S.tmp] + 1}`：现在是 `None` → 直接更新' if S.f[S.now] is None
                                                 else f'比较：现有 `f[{S.now}] = {S.f[S.now]}`，这条路 `f[{S.tmp}] + 1 = {S.f[S.tmp] + 1}`'),
        'f[now] = f[tmp] + 1': '更新 `f[{now}] = f[{tmp}] + 1` = =={f[now]}==',
        'return f[now]': '`f[{now}] = {ret}`：拼出这个状态里的字母最少要 `{ret}` 张',
    },
    max_steps=90,
    cards=dict(
        one_liner='用位表示 target 里哪些字母已拼出，记忆化 DFS 求最少贴纸数',
        complexity='时间约 `O(2^n × 贴纸数 × 字母数)`，空间 `O(2^n)`（n = len(target) ≤ 15）',
        problem=['有若干种贴纸（每种无限张），每张贴纸上是小写字母，可以剪下字母重新排列',
                 '求拼出 `target` 最少需要几张贴纸，拼不出返回 `-1`',
                 '本视频：`stickers = ["ab","bc"], target = "abbc"` → `2`'],
        quote='题目保证target的长度不超过15，因此可以使用状态压缩动态规划来做。具体来说就是对于target中的第index个字母，将其编码为2^index',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[status]` = 拼出 status 代表的字母最少要几张贴纸；`f[0] = 0`',
              '每次从还没拼的字母里选==一个==，只枚举含它的贴纸，把贴纸能盖住的字母都去掉，得到新状态 `tmp`',
              '递归求 `f[tmp]`，用 `f[tmp] + 1` 更新 `f[status]`；`f` 同时是记忆化缓存'],
        summary=['时间约 `O(2^n × 贴纸数 × 字母数)`，空间 `O(2^n)`',
                 '只枚举含「某个未拼字母」的贴纸，比枚举所有贴纸剪枝得多',
                 '`pos_dict` 记每个字母已用掉几个位置，保证同一字母按顺序盖住',
                 '拼不出（target 里有贴纸里没有的字母）直接返回 `-1`',
                 '原文为 Python 2 写法，`tmp.items()` 在 Python 3 里是视图，遍历结果相同，没有改动代码'],
    ),
)
