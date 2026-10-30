def _diff(S):
    q, s = S.get('q'), S.get('s')
    if q is None or s is None:
        return None
    return [i for i, (x, y) in enumerate(zip(q, s)) if x != y]


def _txt(S):
    d = _diff(S)
    if d is None:
        return '对每个 query，逐个和字典单词比较：至多 2 个位置不同就算成功'
    q, s = S['q'], S['s']
    return f"`{q}` 对 `{s}`：不同位置 {d if d else '无'}，共 =={len(d)}== 处 → " + ('==≤ 2，成功==' if len(d) <= 2 else '> 2，不行')


def _if(S, B, ret):
    d = _diff(S)
    q, s = S.q, S.s
    if len(d) <= 2:
        return f'`{q}` 和 `{s}` 有 {len(d)} 个位置不同 `≤ 2` → ==两次编辑内能变成它=='
    return f'`{q}` 和 `{s}` 有 {len(d)} 个位置不同 `> 2` → 换字典里的下一个单词'


CONFIG = dict(
    num=2452, title='距离字典两次编辑以内的单词', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='暴力枚举 · 统计不同字母数',
    tags=[],
    code='''
class Solution:
    def twoEditWords(self, queries: List[str], dictionary: List[str]) -> List[str]:
        ans = []
        for q in queries:
            for s in dictionary:
                if sum(x != y for x, y in zip(q, s)) <= 2:
                    ans.append(q)
                    break
        return ans
''',
    call='Solution().twoEditWords(["word","note","ants","wood"], ["wood","joke","moat"])',
    expect=["word", "note", "wood"],
    views=[
        dict(type='text', fn=_txt, size=28, h=90),
        dict(type='array', var='queries', label='queries（蓝 = 当前 q）', cell=130, h=170,
             color=lambda S, i, v: 'blue' if v == S.get('q') else ('green' if v in S.get('ans', []) else None)),
        dict(type='array', var='dictionary', label='dictionary（粉 = 当前 s）', cell=130, h=170,
             color=lambda S, i, v: 'pink' if v == S.get('s') else None),
        dict(type='array', var='ans', label='ans', cell=130, h=170, color=lambda S, i, v: 'green'),
    ],
    watch=[('q', 'q', 'blue'), ('s', 's', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = []': '`ans` 收集满足条件的 query，保持原顺序',
        'for q in queries': lambda S, B, r: ('queries 遍历完了' if S.q == B.get('q') else f'取下一个 `q = {S.q!r}`，去字典里找能在两次编辑内变成的单词'),
        'for s in dictionary': lambda S, B, r: (f'字典看完了，`{S.q}` 没有合适的单词 → 不入答案' if S.s == B.get('s') and S.s == S.dictionary[-1] else f'拿字典里的 `s = {S.s!r}` 和 `q` 比'),
        'if sum(': _if,
        'ans.append(q)': '`{q!r}` 满足条件，加入答案：`ans = {ans}`',
        'break': '找到一个就够了，不用再看字典后面的 → 去下一个 query',
        'return ans': '字典全看完没找到的 query 自然就没加入。返回 `{ans}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='两个等长单词至多 2 个位置不同，就能两次编辑内变成',
        complexity='时间 `O(q·d·n)`，空间 `O(1)`（返回值不计）',
        problem=['一次编辑 = 把 query 的任意一个字母改成别的字母',
                 '找出能在 ==不超过 2 次编辑== 内变成字典中某个单词的 query，保持原顺序',
                 '示例：`["word","note","ants","wood"]`，字典 `["wood","joke","moat"]` → `["word","note","wood"]`'],
        quote='对于每个 q = queries[i]，遍历 dictionary 中的字符串 s，判断 q 和 s 是否至多有两个位置上的字母不同。',
        quote_src='—— 灵茶山艾府题解',
        idea=['等长单词，编辑次数 = ==对应位置不同的字母个数==',
              '`sum(x != y for x, y in zip(q, s))` 一行数出不同位置数',
              '`≤ 2` 就加入答案并 `break`，换下一个 query'],
        summary=['时间 `O(q·d·n)`，数据只有 100，暴力足够',
                 '易错：找到后要 `break`，否则同一个 query 会被重复加入',
                 '`x != y` 是布尔值，`sum` 直接把 True 当 1 累加'],
    ),
)
