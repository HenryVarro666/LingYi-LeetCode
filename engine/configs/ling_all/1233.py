def _cmp(S):
    if 'last' not in S:
        return '排序后：子文件夹一定排在它的上级文件夹后面'
    s, last = S['s'], S['last']
    if s.startswith(last) and len(s) > len(last):
        nxt = s[len(last)]
        if nxt == '/':
            return f"`{s}` 以 `{last}` 开头，下一个字符是 ==/== → 是子文件夹，删掉"
        return f"`{s}` 以 `{last}` 开头，但下一个字符是 ==`{nxt}`== 不是 `/` → 不是子文件夹，保留"
    return f"`{s}` 不以 `{last}` 开头 → 不是子文件夹，保留"


def _col(S, i, v):
    if 's' not in S:
        return None
    if v == S['s']:
        return 'blue'
    if v == S.get('last'):
        return 'pink'
    return None


CONFIG = dict(
    num=1233, title='删除子文件夹', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='排序 + 比较上一个保留的路径',
    tags=['字典树（trie）'],
    code='''
class Solution:
    def removeSubfolders(self, folder: List[str]) -> List[str]:
        folder.sort()
        ans = [folder[0]]
        for s in folder[1:]:  # 切片可以用 for i in range(1, n) 代替，做到 O(1) 空间
            last = ans[-1]
            if not s.startswith(last) or s[len(last)] != '/':
                ans.append(s)
        return ans
''',
    call='Solution().removeSubfolders(["/c/d", "/a/b", "/c/d/e", "/ab", "/a", "/c/f"])',
    expect=['/a', '/ab', '/c/d', '/c/f'],
    views=[
        dict(type='array', var='folder', label='folder（排序后；蓝 = 当前 s，粉 = last）', cell=150, h=240, color=_col),
        dict(type='array', var='ans', label='ans（保留的文件夹）', cell=150, h=240),
        dict(type='text', h=110, size=30, fn=_cmp),
    ],
    watch=[('s', 's', 'blue'), ('last', 'last', 'pink'), ('len(ans)', 'len(ans)', 'green')],
    captions={
        'folder.sort()': '先按字典序排序：==上级文件夹一定排在它的子文件夹前面==',
        'ans = [folder[0]]': '排序后第一个不可能是别人的子文件夹，直接保留',
        'for s in folder[1:]': '`s` = `{s}`',
        'last = ans[-1]': '只和==上一个未被删除的路径== `{last}` 比较，不用和更早的比',
        'if not s.startswith': lambda S, B, r: _cmp(S),
        'ans.append(s)': '`{s}` 不是子文件夹 → 加入 ans，它成为新的 last',
        'return ans': '剩下的文件夹：`{ans}`',
    },
    cards=dict(
        one_liner='排序后，只需和上一个没被删的路径比前缀',
        complexity='时间 `O(l·n log n)`，空间 `O(1)`',
        problem=['`folder` 是一组路径，删掉所有「位于别的文件夹之下」的子文件夹',
                 '`/a/b` 是 `/a` 的子文件夹，但 `/ab` 不是（前缀后面要跟 `/`）',
                 '示例：`["/a","/a/b","/c/d","/c/d/e","/c/f"]` → `["/a","/c/d","/c/f"]`'],
        quote='如果 folder 列表是有序的，那么当 B 是 A 的子文件夹时，A 是 B 的前缀，所以 A 一定排在 B 的左边。',
        quote_src='—— 灵茶山艾府题解',
        idea=['暴力枚举两两比较要 `O(l·n²)`，太慢',
              '排序后上级一定在前，只需比较当前路径与==上一个未被删除的路径==',
              '判断 `A + "/"` 是前缀：先 `startswith(A)`，再看 `s[len(A)]` 是否为 `/`（题目保证不重复，不会越界）'],
        summary=['排序 `O(n log n)` 次比较，每次比较 `O(l)`',
                 '易错：只判断 `startswith` 会把 `/ab` 误当成 `/a` 的子文件夹，必须再检查 `/`',
                 '不用和更早的路径比：若它是更早路径的子文件夹，上一个路径也会是，早已被删',
                 '切片 `folder[1:]` 可改成下标循环做到 `O(1)` 空间'],
    ),
)
