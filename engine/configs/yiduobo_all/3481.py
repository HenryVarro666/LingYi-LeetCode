REPL = [['A', '%B%%B%'], ['B', 'x%C%'], ['C', 'y']]
TEXT = '%A%-%C%'


def _info(S):
    if 'key' not in S or 'value' not in S:
        return '先给每个 key 算出「去掉所有占位符后」的最终字符串，存进 `mapping`'
    return f"正在求 key = =={S['key']}==，value = `{S['value']}`"


CONFIG = dict(
    num=3481, title='应用替换', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='递归求每个 key 的最终串 + 一趟替换 text',
    tags=['灵神题单', '拓扑排序'],
    code='''
class Solution(object):
    def applySubstitutions(self, replacements, text):
        
        mapping = {}
        replacements_dict = {}
        for key, value in replacements:
            replacements_dict[key] = value

        def get(key, value, mapping):
            if key not in mapping:
                parts = []
                p = 0
                while p < len(value):
                    if value[p] == '%':
                        parts.append(get(value[p + 1], replacements_dict[value[p + 1]], mapping))
                        p += 3
                    else:
                        parts.append(value[p])
                        p += 1
                
                mapping[key] = ''.join(parts)
            
            return mapping[key]

        for key, value in replacements:
            if key not in mapping:
                get(key, value, mapping)
        
        res = []
        p = 0
        while p < len(text):
            if text[p] == '%':
                res.append(mapping[text[p + 1]])
                p += 3
            else:
                res.append(text[p])
                p += 1
        
        return ''.join(res)
''',
    call=f'Solution().applySubstitutions({REPL}, {TEXT!r})',
    expect='xyxy-y',
    views=[
        dict(type='map', var='replacements_dict', label='replacements_dict（key → 原始 value）', fmt=lambda k, v: f"'{k}': '{v}'", h=130, font=28),
        dict(type='map', var='mapping', label='mapping（key → 去掉占位符后的最终串）', fmt=lambda k, v: f"'{k}': '{v}'", h=130, font=28),
        dict(type='text', h=80, size=30, fn=_info),
        dict(type='string', var='text', label='text（第二趟：扫描并替换）', pointers={'(res, p)[1]': 'blue'}, cell=90, h=200),
        dict(type='calls', h=250),
    ],
    watch=[('p', 'p', 'blue'), ('parts', "''.join(parts)", 'green')],
    skip=['replacements_dict[key] = value', 'p = 0', 'parts = []'],
    captions={
        'mapping = {}': '`mapping` 将存放每个 key 的最终字符串',
        6: '先把 `[key, value]` 存成查找表 `replacements_dict`，递归时要用',
        25: lambda S, B, r: f'逐个处理 `[{S.key}, {S.value}]`',
        'if key not in mapping': lambda S, B, r: (f'`{S.key}` 还没算过 → 现在去算' if S.key not in S.mapping
                                                 else f'`{S.key}` 已在 `mapping` 里 → 直接复用'),
        'while p < len(value)': lambda S, B, r: (f'`p = {S.p}` 还在 value 内，继续扫' if S.p < len(S.value) else '`value` 扫完了'),
        "if value[p] == '%'": lambda S, B, r: (f'`value[{S.p}]` 是 `%`，下一个字符 `{S.value[S.p + 1]}` 是另一个 key，要先求它'
                                              if S.value[S.p] == '%' else f'`value[{S.p}] = {S.value[S.p]!r}` 是普通字符，直接收下'),
        'parts.append(get': '递归求被引用 key 的最终串，把结果加入 `parts`',
        'p += 3': '跳过 `%X%` 三个字符：`p` → {p}',
        'p += 1': '`p` → {p}',
        "mapping[key] = ": "`mapping['{key}']` = =={mapping[key]}==，以后不用再算",
        'return mapping[key]': '返回 `{key}` 的最终串 =={mapping[key]}==',
        'res.append(mapping': '`%{text[p + 1]}%` 换成 `mapping` 里的 =={mapping[text[p + 1]]}==',
        'res.append(text[p])': '普通字符原样保留',
        'return \'\'.join(res)': "第二趟结束，返回 =={''.join(res)}==",
    },
    cards=dict(
        one_liner='先算出每个 key 的最终串，再扫一遍 text 替换',
        complexity='时间 `O(L·2^n)`，空间 `O(L·2^n)`',
        problem=['`replacements` 是 `[key, value]` 列表，`value` 可含 `%X%` 占位符，无循环依赖',
                 '把 `text` 里的占位符全部替换掉',
                 '示例：A=`%B%%B%`，B=`x%C%`，C=`y`，text=`%A%-%C%` → `xyxy-y`'],
        quote='使用一个哈希表mapping记录每种key对应的去除掉所有占位符后得到的最终字符串',
        quote_src='—— yiduobo 题解原文',
        idea=['`get(key, value)`：从 value 头扫到尾，遇到 `%` 就递归求被引用 key',
              '求出的最终串存进 `mapping`，同一个 key 只算一次',
              '所有 key 都有最终串后，对 `text` 做同样的扫描替换'],
        summary=['时间、空间 `O(L·2^n)`，结果可能指数级长',
                 '`%X%` 占 3 个字符，所以 `p += 3`',
                 '`mapping` 起到记忆化作用，避免重复展开',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改',
                 '对比灵神：灵神一个 `dfs(s)` 直接展开字符串；这里把「求 key」和「替换 text」分成两步'],
    ),
)
