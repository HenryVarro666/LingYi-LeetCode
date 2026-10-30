CONFIG = dict(
    num=3734, title='大于目标字符串的最小字典序回文排列', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='构造左半 · 顶着 target 填再回溯',
    tags=['灵神题单', '贪心与思维', '难度分 2330'],
    code='''
class Solution(object):
    def lexPalindromicPermutation(self, s, target):
        
        cnt = {}
        for c in s:
            cnt[c] = cnt.get(c, 0) + 1
        
        mid = ""
        for c in cnt:
            if cnt[c] % 2 == 1:
                if mid != "":
                    return ""
                mid = c
            cnt[c] //= 2
        
        half = []
        p = len(target) // 2 - 1
        for i in range(len(target) // 2):
            if cnt.get(target[i], 0) > 0:
                half.append(target[i])
                cnt[target[i]] -= 1
            else:
                p = i
                break

        if len(half) == len(target) // 2:
            s = ''.join(half) + mid + ''.join(half[::-1])
            if s > target:
                return s
            
            if half:
                cnt[half.pop()] += 1

        while p >= 0:
            for i in range(ord(target[p]) + 1, 123):
                c = chr(i)
                if cnt.get(c, 0) > 0:
                    half.append(c)
                    cnt[c] -= 1
                
                    for j in range(26):
                        c = chr(j + 97)
                        while cnt.get(c, 0) > 0:
                            half.append(c)
                            cnt[c] -= 1
                    
                    return ''.join(half) + mid + ''.join(half[::-1])
            
            if half:
                cnt[half.pop()] += 1
            p -= 1
        
        return ""
''',
    call='Solution().lexPalindromicPermutation("baba", "abba")',
    expect='baab',
    skip=['for i in range(ord(target[p])', 'c = chr(i)', 'if cnt.get(c, 0) > 0:', 'for j in range(26)', 'c = chr(j + 97)', 'while cnt.get(c, 0) > 0'],
    views=[
        dict(type='string', var='target', label='target（左半是要填的部分；蓝 = 位置 p）', cell=100, h=170,
             pointers={'p': 'blue'}, color=lambda S, k, v: 'blue' if S.get('p') == k else None,
             dim=lambda S, k, v: k >= len(S['target']) // 2),
        dict(type='array', var='half', label='half（左半；绿 = 刚填的）', cell=90, h=150,
             color=lambda S, k, v: 'green' if k == len(S['half']) - 1 else None),
        dict(type='map', var='cnt', label='cnt（左半还能用的字母数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=34),
        dict(type='text', fn=lambda S: (f"正中间字母 `mid = '{S['mid']}'`" if 'mid' in S else ''), size=28, h=80),
    ],
    watch=[('p', 'p', 'blue'), ('mid', 'mid', 'green'), ('i', 'i'), ('c', 'c', 'orange')],
    captions={
        'cnt = {}': '`cnt` 统计每个字母的次数',
        'cnt[c] = cnt.get': '`cnt = {cnt}`',
        'mid = ""': '`mid` 记下出现奇数次的字母（放正中间）',
        'for c in cnt': '看字母 `{c!r}`：共 `{cnt[c]}` 次',
        'if cnt[c] % 2 == 1': lambda S, B, r: (f"`{S.c!r}` 出现奇数次，只能放正中间" if S.cnt[S.c] % 2 == 1 else f"`{S.c!r}` 出现偶数次，成对摆放"),
        'if mid != ""': lambda S, B, r: ('已经有奇数次字母了 → 超过一个，无法回文' if S.mid != '' else '第一个奇数次字母，没问题'),
        'mid = c': '`mid = {mid!r}`',
        'cnt[c] //= 2': '次数除以 2 = 左半能用几个：`{c!r}` → `{cnt[c]}`',
        'half = []': '`half` 是回文的==左半==，先顶着 target 的左半填',
        'p = len(target) // 2 - 1': '`p` 默认是左半最后一位 `{p}`',
        'for i in range(len(target) // 2)': lambda S, B, r: ('左半照抄循环结束' if len(S.half) >= len(S.target) // 2 else f"`i = {S.i}`：看 `target[{S.i}] = '{S.target[S.i]}'` 还有没有"),
        'if cnt.get(target[i], 0) > 0': lambda S, B, r: (f"`{S.target[S.i]}` 还有剩余 → 照抄" if S.cnt.get(S.target[S.i], 0) > 0 else f"`{S.target[S.i]}` 没有剩余了 → 从这里开始调整"),
        'half.append(target[i])': '`half` → `{"".join(half)}`',
        'cnt[target[i]] -= 1': '用掉一个 `{target[i]}`',
        'p = i': '`p = {p}`：从这里往前找能变大的位置',
        'if len(half) == len(target) // 2': lambda S, B, r: ('左半照抄完整：先试镜像后是否大于 target' if len(S.half) == len(S.target) // 2 else '没抄完整，直接去调整'),
        's = \'\'.join(half)': '镜像后的回文 `{s}`',
        'if s > target': lambda S, B, r: (f"`{S.s}` > `{S.target}`：直接就是答案" if S.s > S.target else f"`{S.s}` <= `{S.target}`：不够大，要把左半最后一位变大"),
        'if half': '`half` 末位要弹出来重选',
        'cnt[half.pop()] += 1': '弹出 `half` 末位并还回 `cnt`：`half = {"".join(half)}`',
        'while p >= 0': '尝试在位置 `p = {p}` 填比 `target[{p}] = {target[p]!r}` 更大的字母',
        'half.append(c)': lambda S, B, r: f"找到更大的可用字母 `{S.c}`：`half` → `{''.join(S.half)}`" if S.get('_line') == 38 else f"`half` 补上 `{S.c}` → `{''.join(S.half)}`",
        'cnt[c] -= 1': '用掉一个 `{c}`',
        'return \'\'.join(half)': '左半 + 中间 + 左半翻转 = `{ret!r}`',
        'p -= 1': '这一位没有更大的字母 → 回溯，`p` → {p}',
        'return ""': '无解，返回空串',
    },
    max_steps=80,
    cards=dict(
        one_liner='先造左半：顶着 target 填，填不大就退一位再换',
        complexity='时间 `O(n + |Σ|)`，空间 `O(n)`',
        problem=['把 `s` 重排成==回文串==，要求严格大于 `target` 且字典序最小，没有返回 `""`',
                 '示例：`s = "baba"`，`target = "abba"` → `"baab"`',
                 '回文排列只有 `abba` 和 `baab`'],
        quote='无论是哪种情况，都期望得到一个字典序最小，且大于等于target的前半部分的字符串，那么就可以从最左侧开始，顶着target的前半部分逐个字符填充答案字符串。',
        quote_src='—— yiduobo 题解原文',
        idea=['奇数次的字母超过一个就无解；恰好一个放 `mid`；次数除以 2 得左半能用的字母',
              '左半顶着 `target` 的左半填；填满后镜像，若已大于 `target` 直接返回',
              '否则从后往前弹出字母，在该位找更大的字母，剩余从小到大补满，再镜像'],
        result='`ab` 镜像是 `abba`，不大于 target；弹到 `a` 换成 `b`，补 `a` → 左半 `ba` → `baab` ✓',
        summary=['时间 `O(n + |Σ|)`，空间 `O(n)`',
                 '镜像 `s > target` 时必须严格大于，等于也要继续调整',
                 '左半没抄完时，`p` 就是第一个“抄不下去”的位置',
                 '与灵神对比：灵神用 neg 和 left_max 倒着判断；yiduobo 顺着填，再回溯弹出',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
