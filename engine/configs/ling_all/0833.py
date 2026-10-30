CONFIG = dict(
    num=833, title='字符串中的查找与替换', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='先记录替换，再一次扫描拼接',
    code='''
class Solution:
    def findReplaceString(self, s: str, indices: List[int], sources: List[str], targets: List[str]) -> str:
        replace = [(c, 1) for c in s]
        for i, src, tar in zip(indices, sources, targets):
            if s.startswith(src, i):  # 判断 s[i:] 的前缀是否为 src，这样写无需切片
                replace[i] = (tar, len(src))  # (替换后的字符串，被替换的长度)

        ans = []
        i = 0
        while i < len(s):
            ans.append(replace[i][0])  # 替换后的字符串（默认为 s[i]）
            i += replace[i][1]  # 被替换的长度（默认为 1）
        return ''.join(ans)
''',
    call='Solution().findReplaceString("abcdef", [0, 2, 4], ["ab", "ec", "ef"], ["eee", "ffff", "g"])',
    expect='eeecdg',
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前下标 i）', cell=84, pointers={'i': 'blue'}, h=200,
             color=lambda S, k, v: 'blue' if S.get('i') == k and 'ans' in S else None),
        dict(type='text', size=26, h=80, fn=lambda S: '替换表：' + (('，'.join(f"`{k}`: `{S['s'][k:k+t[1]]}`→==`{t[0]}`==" for k, t in enumerate(S['replace']) if t[1] != 1 or t[0] != S['s'][k]) or '（暂无）') if 'replace' in S else '')),
        dict(type='text', size=26, h=80, fn=lambda S: ('ans：' + ' + '.join(f'`{x}`' for x in S['ans'])) if S.get('ans') else ''),
    ],
    watch=['i', ('ans', 'ans', 'green')],
    captions={
        'replace = [': '先给每个位置一个默认值 `(s[i], 1)`：原样保留，长度 1',
        'for i, src, tar': lambda S, B, r: ('所有操作都登记完了，退出循环' if B.get('src') == S.get('src') and 'src' in B and B.get('i') == S.get('i') else f"第 {S.indices.index(S.i)+1} 个操作：下标 `{S.i}`，要找 `{S.src}`，换成 `{S.tar}`"),
        's.startswith': lambda S, B, r: (f"`s[{S.i}:]` 以 `{S.src}` 开头吗？" + ('==是==，可以替换' if S.s.startswith(S.src, S.i) else '==不是==，什么也不做')),
        'replace[i] = ': '记录 `replace[{i}] = ({tar!r}, {len(src)})`：这里换成 `{tar}`，并跳过 `{len(src)}` 个字符',
        'ans = []': '第二阶段：按 `replace` 从左到右扫描原串拼答案',
        'i = 0': '`i` 从 0 开始',
        'while i < len': lambda S, B, r: (f'`i = {S.i} < {len(S.s)}`，继续' if S.i < len(S.s) else f'`i = {S.i}` 已到末尾，结束'),
        'ans.append': '取 `replace[{i}][0] = {replace[i][0]!r}` 加入答案',
        'i += replace': lambda S, B, r: f"`i` 跳过 `{S.replace[B.i][1]}` 个字符 → {S.i}（被替换的那段不再逐个看）",
        'return': '拼接得到 `{ret}`',
    },
    cards=dict(
        one_liner='先记下哪里要替换，再从左到右一次拼出答案',
        complexity='时间 `O(L)`，空间 `O(L)`，`L` 为所有字符串长度之和',
        problem=['给 `s` 和 `k` 组 `(indices, sources, targets)`：若 `s` 从 `indices[i]` 起以 `sources[i]` 开头，就换成 `targets[i]`',
                 '所有替换==同时==发生，基于原字符串，且互不重叠',
                 '示例：`abcd`，`[0,2]`，`["a","cd"]`，`["eee","ffff"]` → `eeebffff`'],
        quote='如果从 indices[i] 开始的字符串有前缀 sources[i]，则可以替换成 target[i]。此时记录 replace[indices[i]] = (target[i], len(sources[i]))，表示替换后的字符串，以及被替换的长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`replace[i]` 默认是 `(s[i], 1)`，匹配成功就改成 `(tar, len(src))`',
              '`startswith(src, i)` 直接从下标 `i` 比较，不用切片',
              '扫描时加入 `replace[i][0]`，再跳 `replace[i][1]` 格，被替换的区间一次跳过'],
        summary=['时间 `O(L)`：每次匹配只比较 `len(sources[i])` 个字符',
                 '易错：必须基于==原串==下标，不能边替换边改 `s`',
                 '`replace[i][1]` 是被替换的长度，不是 `len(tar)`',
                 '与 yiduobo 的排序后边拼边走不同：这里用数组按位置登记，无需排序'],
    ),
)
