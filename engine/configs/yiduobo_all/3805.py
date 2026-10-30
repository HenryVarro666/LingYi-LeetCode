WORDS = ["bcd", "aaa", "yza", "bcd", "zzz", "cde"]


def _idx(S):
    if 'w' not in S or 'cnt' not in S:
        return None
    k = sum(S['cnt'].values()) - (1 if S['_line'] == 9 else 0)
    return k if k < len(S['words']) else None


def _txt(S):
    if 'diff' not in S or _idx(S) is None:
        return '每个字符到首字符的距离 `diff` 在轮转中==不变==：diff 相同 ⇔ 相似'
    w = S['w']
    parts = ', '.join(f"({c}−{w[0]})%26={(ord(c) - ord(w[0])) % 26}" for c in w[1:])
    return f"`{w}`：`{parts}` → `diff = {S['diff']}`"


CONFIG = dict(
    num=3805, title='统计凯撒加密对数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='到首字符的距离数组 + 哈希计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1624'],
    code='''
class Solution(object):
    def countPairs(self, words):
        
        cnt = {}
        res = 0
        for w in words:
            diff = tuple([(ord(c) - ord(w[0])) % 26 for c in w[1:]])
            v = cnt.get(diff, 0)
            res += v
            cnt[diff] = v + 1
        
        return res
''',
    call=f'Solution().countPairs({WORDS})',
    expect=7,
    views=[
        dict(type='array', var='words', label='words', h=170, cell=110, index=True,
             color=lambda S, i, v: 'blue' if i == _idx(S) else None,
             dim=lambda S, i, v: _idx(S) is not None and i > _idx(S)),
        dict(type='text', h=90, size=28, fn=_txt),
        dict(type='map', var='cnt', label='cnt（diff → 已出现次数）', fmt=lambda k, v: f'{k}: {v}', h=160, font=34),
    ],
    watch=[('w', 'w', 'blue'), ('diff', 'diff'), ('v', 'v', 'orange'), ('res', 'res', 'green')],
    captions={
        'cnt = {}': '`cnt` 记录遍历过的串中每种 `diff` 出现的次数',
        'res = 0': '`res` 累计相似的下标对',
        'for w in words': lambda S, B, r: (f'遍历到 `{S.w!r}`' if _idx(S) is not None else '遍历完成'),
        'diff = tuple(': '各字符到首字符 `{w[0]!r}` 的距离：`diff = {diff}`（`% 26` 处理 z → a 的轮转）',
        'v = cnt.get(diff, 0)': lambda S, B, r: (f'之前有 `v = {S.v}` 个串的 diff 也是 `{S.diff}` → 都和 `{S.w!r}` 相似' if S.v
                                                else f'之前没有 diff 为 `{S.diff}` 的串'),
        'res += v': '`res` += `{v}` → =={res}==',
        'cnt[diff] = v + 1': '`{diff}` 的次数加 1 → `{cnt[diff]}`',
        'return res': '共 `{res}` 对',
    },
    cards=dict(
        one_liner='轮转不改变“到首字符的距离”，按距离数组分组计数',
        complexity='时间 `O(nm)`，空间 `O(nm)`',
        problem=['一次操作把串的==每个字母==都变成下一个（z → a）',
                 '两个串能通过操作变相等就==相似==，求相似的 `(i < j)` 对数',
                 '示例：`["ab","aa","za","aa"]` → `2`',
                 f'本视频：`["bcd","aaa","yza","bcd","zzz","cde"]` → `7`'],
        quote='无论如何轮转，字符串中的==每个字符与首字符的距离都是不变的==，因此可以将每个字符串都转化为其中所有字符到首字符的距离的数组diff。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个串的 `diff` 相同 ⇔ 能通过操作互相转换',
              '`diff` 只存后 `m − 1` 个字符，转成 `tuple` 才能当哈希键',
              '一趟遍历：先查 `cnt[diff]` 累加，再把它加 1'],
        summary=['时间 `O(nm)`，空间 `O(nm)`',
                 '`(ord(c) − ord(w[0])) % 26`：取模让 `yza` 和 `abc` 得到相同 diff',
                 '先用旧次数更新 `res`，再加 1，避免自己和自己配对',
                 '原文为 Python 2 风格，代码无需改动即可运行'],
    ),
)
