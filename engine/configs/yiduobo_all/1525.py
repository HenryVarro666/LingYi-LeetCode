TRACK = '''
class KStr(str):
    pass

class TStr(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield str.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KStr(str(self))
        c.k = getattr(self, 'k', -1)
        return c
'''


def _k(S):
    k = getattr(S.get('s'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _color(S, i, v):
    k = _k(S)
    if k is None or 'left' not in S:
        return None
    return 'blue' if i <= k else 'pink'


def _txt(S):
    if 'left' not in S or 'right' not in S or _k(S) is None:
        return '左边不同字符数 `len(left)`，右边不同字符数 `len(right)`'
    a, b = len(S['left']), len(S['right'])
    return f'`len(left)` = =={a}==，`len(right)` = =={b}==' + ('，==相等，好分割==' if a == b else '')


CONFIG = dict(
    num=1525, title='字符串的好分割数目', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='集合 + 哈希表计数 · 一趟扫描',
    tags=['动态规划'],
    code='''
class Solution(object):
    def numSplits(self, s):

        left = set()
        right = {}
        for char in s:
            right[char] = right.get(char, 0) + 1
        
        res = 0
        for char in s:
            left.add(char)
            right[char] -= 1
            if right[char] == 0:
                right.pop(char)
            
            if len(left) == len(right):
                res += 1
        
        return res
''',
    setup=TRACK,
    call="Solution().numSplits(TStr('aacaba'))",
    expect=2,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='string', var='s', pointers={_k: 'yellow'}, pointer_labels={_k: 'char'}, color=_color, h=200,
             label='s（蓝 = 左半，粉 = 右半，切在黄色字符之后）'),
        dict(type='set', var='left', h=200, label='left：左半出现过的字符'),
        dict(type='map', var='right', h=250, label='right：右半各字符的个数'),
    ],
    watch=[('char', 'char', 'yellow'), ('res', 'res', 'green')],
    captions={
        'left = set()': '`left` 集合：记录左半出现过哪些字符',
        'right = {}': '`right` 哈希表：记录右半每个字符还剩几个',
        'for char in s': lambda S, B, r: ((f'第一趟：把 `{S.char}` 计入右半' if _k(S) is not None else '第一趟结束：`right` 里是整个 s 的字符计数') if 'res' not in S
                                          else (f'切在下标 {_k(S)} 之后：`{S.char}` 从右半移到左半' if _k(S) is not None else '扫描结束')),
        'right[char] = right.get': '`right[{char}]` = =={right.get(char)}==：开始时整个 s 都在右半',
        'res = 0': '`res` 统计好分割个数',
        'left.add': '`{char}` 加入左半：`left` = {sorted(left)}',
        'right[char] -= 1': '`{char}` 离开右半：`right[{char}]` = =={right[char]}==',
        'if right[char] == 0': lambda S, B, r: (f'`{S.char}` 在右半个数为 0 → 右半不再有它，要删掉' if S.right[S.char] == 0
                                                else f'`{S.char}` 在右半还有 {S.right[S.char]} 个，保留'),
        'right.pop': '删掉 `{char}`：`len(right)` 才是右半不同字符数 = =={len(right)}=='
                     ,
        'if len(left) == len(right)': '左 `{len(left)}` 种，右 `{len(right)}` 种：{"==相等，这是个好分割==" if len(left)==len(right) else "不相等，继续"}',
        'res += 1': '好分割 +1，`res` = =={res}==',
        'return res': '一共 `{res}` 个好分割',
    },
    cards=dict(
        one_liner='左边用集合、右边用计数表，边切边比不同字符数',
        complexity='时间 `O(n)`，空间 `O(k)`（k 为字符种类数）',
        problem=['把字符串 `s` 切成非空的 `p` 和 `q` 两段',
                 '若两段里不同字符的数目相同，就是一个「好分割」，求个数',
                 '示例：`aacaba` → `2`（`aac|aba` 和 `aaca|ba`）'],
        quote='从左向右一趟扫描，枚举每种分割的情况。对于每种情况，判断左侧和右侧中不同字符的数目即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先扫一遍，把所有字符数进 `right`，此时左半为空',
              '再扫一遍，每个字符从右半挪到左半：`left` 加入，`right` 减 1',
              '计数减到 0 就 `pop`，于是 `len(right)` 就是右半不同字符数'],
        summary=['时间 `O(n)`，空间 `O(1)`（最多 26 种字符）',
                 '易错：计数为 0 必须 `pop`，否则 `len(right)` 会偏大',
                 '最后一个位置切完后右半为空，`len(left) ≥ 1` 不会误判',
                 '原文本身是 Python 3 可运行的，没有改动；题面库里缺失，按题意补写'],
    ),
)
