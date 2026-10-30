REPL = [['A', '%B%%B%'], ['B', 'x%C%'], ['C', 'y']]
TEXT = '%A%-%C%'


def _res(S):
    if 's' not in S:
        return '`replace` 把 key 映射到 value；value 里的 `%X%` 要继续展开'
    return f"当前展开 `{S['s']}`，已拼出 =={''.join(S['res']) or '（空）'}==（i = {S['i']}）"


CONFIG = dict(
    num=3481, title='应用替换', difficulty='Medium', category='图论算法',
    author='灵茶山艾府', technique='记忆化递归展开占位符',
    tags=['灵神题单', '拓扑排序'],
    code='''
class Solution:
    def applySubstitutions(self, replacements: List[List[str]], text: str) -> str:
        replace = dict(replacements)
        @cache
        def dfs(s: str) -> str:
            res = []
            i, n = 0, len(s)
            while i < n:
                if s[i] != '%':
                    res.append(s[i])
                    i += 1
                else:
                    res.append(dfs(replace[s[i + 1]]))
                    i += 3
            return ''.join(res)
        return dfs(text)
''',
    call=f'Solution().applySubstitutions({REPL}, {TEXT!r})',
    expect='xyxy-y',
    views=[
        dict(type='map', var='replace', label='replace（key → value）', fmt=lambda k, v: f"'{k}': '{v}'", h=170, font=30),
        dict(type='string', var='s', label='当前正在展开的字符串 s', pointers={'i': 'blue'}, cell=90, h=190),
        dict(type='text', h=90, size=30, fn=_res),
        dict(type='calls', h=300),
    ],
    watch=[('i', 'i', 'blue'), ('res', "''.join(res)", 'green')],
    captions={
        'replace = dict': '`replace` 记下每个 key 对应的 value',
        'res = []': '新开一层：这一层自己的 `res` 从空开始',
        'res.append(s[i])': '普通字符直接放进结果：`res` = =={"".join(res)}==',
        "if s[i] != '%'": lambda S, B, r: (f'`s[{S.i}] = {S.s[S.i]!r}` 不是 `%` → 普通字符' if S.s[S.i] != '%'
                                           else f'`s[{S.i}]` 是 `%` → 后面 `{S.s[S.i + 1]}` 是占位符，要展开'),
        'res.append(dfs': '递归展开 `{replace[s[i + 1]]}` 得到 `{res[-1]}`；重复的 key 命中 `@cache` 不再重算',
        'i += 3': '跳过 `%X%` 三个字符：`i` → {i}',
        'i += 1': '`i` → {i}',
        'return': "这一层展开完毕，返回 =={''.join(res)}==" ,
    },
    cards=dict(
        one_liner='每个字符串展开一次就缓存，占位符递归替换',
        complexity='时间 `O(L·2^n)`，空间 `O(L·2^n)`（结果本身可以指数级长）',
        problem=['`replacements` 里每项是 `[key, value]`，`value` 可能含 `%X%` 占位符',
                 '把 `text` 里所有占位符反复替换，直到没有占位符',
                 '示例：A=`%B%%B%`，B=`x%C%`，C=`y`，text=`%A%-%C%` → `xyxy-y`'],
        quote='由于 value 长度至多为 8，至多包含 2 个占位符，在最坏情况下，从一个长为 L 的字符串开始，倍增 n-1 次，生成的字符串长度是指数级的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['写一个 `dfs(s)`：把字符串 `s` 里的占位符全部展开',
              '遇到 `%X%` 就递归 `dfs(replace[X])`，再跳过 3 个字符',
              '同一个 value 会被多次展开 → 用 `@cache` 记忆化'],
        summary=['时间、空间都是 `O(L·2^n)`：答案长度本身就可能指数级',
                 '题目保证没有循环依赖，所以递归一定终止',
                 '`%X%` 占 3 个字符，别写成 `i += 2`',
                 '这是拓扑排序题单里的题，递归 + 记忆化等价于按依赖顺序逐个展开'],
    ),
)
