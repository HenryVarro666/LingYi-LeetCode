def _fl(S):
    return list(Counter(S['word']).values())


def _mi_i(S):
    if 'mi' in S and 'freq_list' in S:
        f = _fl(S)
        return f.index(S['mi']) if S['mi'] in f else None
    return None


def _x_i(S):
    if 'x' in S and 'freq_list' in S:
        f = _fl(S)
        return f.index(S['x']) if S['x'] in f else None
    return None


def _txt(S):
    if 'mi' not in S:
        return ''
    return f"枚举最小频率 `mi = {S['mi']}`：允许的频率范围 `[{S['mi']}, {S['mi'] + S['k']}]`"


CONFIG = dict(
    num=3085, title='成为 K 特殊字符串需要删除的最少字符数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='枚举最小频率 · 双重循环算代价',
    tags=['灵神题单', '贪心算法', '难度分 1765'],
    code='''
class Solution(object):
    def minimumDeletions(self, word, k):

        freq_list = Counter(word).values()
        res = None
        for mi in freq_list:
            cost = 0
            for x in freq_list:
                if x < mi:
                    cost += x
                elif x > mi + k:
                    cost += x - (mi + k)
            
            if res is None or res > cost:
                res = cost
        
        return res
''',
    call="Solution().minimumDeletions('dabdcbdcdcd', 2)",
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=32, h=90),
        dict(type='array', var=lambda S: _fl(S), h=300, label='freq_list（各字母的出现次数）',
             color=lambda S, i, v: 'blue' if i == _mi_i(S) else ('yellow' if i == _x_i(S) and S['_line'] >= 9 else None)),
    ],
    watch=[('mi', 'mi', 'blue'), ('x', 'x', 'yellow'), ('cost', 'cost', 'pink'), ('res', 'res', 'green')],
    captions={
        'freq_list = Counter': lambda S, B, r: f"`freq_list` 记录每种字符出现的次数：`{_fl(S)}`（字母 d a b c）",
        'res = None': '`res` 记录最小代价，先设为空',
        'for mi in freq_list': lambda S, B, r: ('所有 mi 都试完了' if B.get('mi') == S.get('mi') and 'mi' in B else f"枚举最小频率 `mi = {S.mi}`：保留下来的字符频率都在 `[{S.mi}, {S.mi + S.k}]`"),
        'cost = 0': '这个 `mi` 下的删除代价从 0 开始',
        'for x in freq_list': lambda S, B, r: ('这个 mi 的所有频率都看完了' if B.get('x') == S.get('x') and 'x' in B else f"看频率 `x = {S.x}` 的这种字符"),
        'if x < mi': '`{x} < {mi}` → {\'比 mi 还少，这种字符只能全删\' if x < mi else \'不比 mi 少\'}',
        'cost += x': '全删，代价加 `{x}`：`cost` = =={cost}==',
        'elif x > mi + k': '`{x} > {mi} + {k} = {mi + k}` → {\'太多了，要减到 mi+k 个\' if x > mi + k else \'在允许范围内，不用删\'}',
        'cost += x - (mi + k)': '多出的要删：`{x} − {mi + k}`，`cost` = =={cost}==',
        'if res is None': '`cost = {cost}`，`res = {B.res}` → {\'更新答案\' if (B.res is None or B.res > cost) else \'不更优\'}',
        'res = cost': '`res` 更新为 =={res}==',
        'return res': '最少删除 `{res}` 个字符',
    },
    cards=dict(
        one_liner='枚举最小频率 mi，其余频率落进 [mi, mi+k]',
        complexity='时间 `O(n + |Σ|²)`，空间 `O(|Σ|)`',
        problem=['任意两种字符的出现次数之差 `<= k`，就是 k 特殊字符串',
                 '求最少删除多少字符，让 `word` 变成 k 特殊字符串',
                 '示例：`word = "dabdcbdcdcd", k = 2` → `2`'],
        quote='从中枚举特殊字符串中字符的最小频率mi，也就是说这个字符串中的所有字符出现频率都必须出现在mi到mi + k之间。',
        quote_src='—— yiduobo 题解原文',
        idea=['对每个 `mi`，再逐个看频率 `x`：`x < mi` 全删，记 `x`',
              '`x > mi + k` 削到 `mi + k`，记 `x − (mi + k)`；否则不动',
              '用每个 `mi` 的代价更新最小值 `res`'],
        summary=['时间 `O(n + |Σ|²)`，空间 `O(|Σ|)`，字符集只有 26',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串；`values()` 在 Python 3 是视图，可重复遍历',
                 '易错：`res` 用 `None` 起步；`x == mi` 时不删',
                 '对比灵神：灵神排序后用滑动窗口优化，这里是朴素双重循环'],
    ),
)
