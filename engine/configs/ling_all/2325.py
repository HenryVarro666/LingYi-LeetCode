_N = [0]


def _txt(S):
    if 'mp' not in S:
        return ''
    if 'c' in S and 'i' in S and S.get('_line') in (5, 6, 7, 8):
        return f'当前 `c = {S["c"]!r}`；下一个还没分配的字母是 `ascii_lowercase[{S["i"]}]` = =={ascii_lowercase[S["i"]]}=='
    return '`mp`：把 key 里的字母按首次出现顺序，映射到 a、b、c…'


def _for(S, B, r):
    _N[0] = _N[0] + 1 if 'c' in B else 1
    if _N[0] > len(S.key):
        return 'key 扫描完了，映射表建好'
    return f'取 key 的下一个字符 `{S.c!r}`'


CONFIG = dict(
    num=2325, title='解密消息', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='哈希表 · 首次出现顺序',
    code='''
class Solution:
    def decodeMessage(self, key: str, message: str) -> str:
        mp = {' ': ' '}
        i = 0
        for c in key:
            if c not in mp:
                mp[c] = ascii_lowercase[i]
                i += 1
        return ''.join(mp[c] for c in message)
''',
    call="Solution().decodeMessage('happy boy', 'hay boy')",
    expect='abd efd',
    views=[
        dict(type='string', var='key', label='key（只取示例前几个字母；真题的 key 含全部 26 个字母）', cell=60, h=170),
        dict(type='map', var='mp', label='mp（黄色 = 刚加入的映射）', fmt=lambda k, v: f"'{k}' → '{v}'", h=330, font=30),
        dict(type='text', size=30, fn=_txt),
    ],
    watch=['i', ('c', 'c', 'blue')],
    captions={
        'mp = {': '先放一个 `{{" ": " "}}`：==空格映射到空格==，后面解密时就不用单独判断空格',
        'i = 0': '`i` 是下一个要分配的字母下标：`ascii_lowercase[0]` = `a`',
        'for c in key': _for,
        'if c not in mp': lambda S, B, r: (f'`{S.c!r}` 还不在 `mp` 里 → ==首次出现==，分配下一个字母' if S.c not in S.mp
                                           else f'`{S.c!r}` 已经在 `mp` 里（不是第一次出现）→ 跳过'),
        'mp[c] = ascii_lowercase[i]': '`mp[{c!r}] = {mp[c]!r}`：key 里第 `{i + 1}` 个新字母对应 `ascii_lowercase[{i}]`',
        'i += 1': '下标加一：下次的新字母对应 `{ascii_lowercase[i] if i < 26 else "无"}`',
        'return': '用 `mp` 逐个翻译 `message`：空格还是空格 → =={ret!r}==',
    },
    cards=dict(
        one_liner='按 key 里字母首次出现的顺序，依次对应 a、b、c…',
        complexity='时间 `O(n + m)`，空间 `O(|Σ|)`',
        problem=['`key` 里 26 个字母==第一次出现的顺序==，对应字母表 a~z，得到替换表',
                 '用替换表翻译 `message`，空格保持不变',
                 '示例：`key = "happy boy"` → `h→a, a→b, p→c, y→d, b→e, o→f`',
                 '本视频：`message = "hay boy"` → `"abd efd"`'],
        quote='把空格映射到空格上，这样就不需要额外判断空格了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历 `key`，字母第一次出现就把它映射到 `ascii_lowercase[i]`，然后 `i += 1`',
              '先在 `mp` 里放 `{" ": " "}`，翻译 `message` 时空格也能直接查表',
              '最后 `"".join(mp[c] for c in message)` 一行完成翻译'],
        summary=['时间 `O(n + m)`，空间 `O(|Σ|)`（`|Σ|` = 27）',
                 '==先放空格映射==：省掉翻译时的 `if c == " "` 判断',
                 '`if c not in mp` 保证只记录==首次==出现的位置',
                 '`ascii_lowercase` 是 `string` 模块里的小写字母表常量',
                 '真题的 key 保证含 26 个字母，所以 `i` 不会越界；视频示例只用了前几个'],
    ),
)
