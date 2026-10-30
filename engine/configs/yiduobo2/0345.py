S0 = 'IceCreAm'
VOW = set('aeiouAEIOU')


def _scan(S):
    """第一个循环里的下标（第二个循环复用了 index 这个名字，那时不显示）"""
    if 'res' in S:
        return None
    return S.get('index')


def _pair(S):
    """第二个循环里正在交换的两个位置"""
    if 'res' not in S or S.get('_line') not in (11, 12, 13):
        return None
    k, n = S.get('index'), S.get('reverse_len')
    if not isinstance(k, int) or k >= n // 2:
        return None
    pl = S['pos_list']
    return pl[k], pl[n - k - 1]


def _a(S):
    p = _pair(S)
    return p[0] if p else None


def _b(S):
    p = _pair(S)
    return p[1] if p else None


def _s_color(S, i, v):
    k = _scan(S)
    if k is None:
        return 'purple' if v in VOW else None
    if i == k:
        return 'orange'
    if i < k and v in VOW:
        return 'purple'
    return None


def _res_color(S, i, v):
    p = _pair(S)
    if p and i in p:
        return 'pink'
    if i in (S.get('pos_list') or []):
        return 'purple'
    return None


def _cap_if(S, B, ret):
    c, i = S.char, S.index
    if c in VOW:
        return f'`s[{i}] = "{c}"` ==是元音==（大小写都算）→ 记下位置 {i}'
    return f'`s[{i}] = "{c}"` 不是元音，跳过'


def _cap_loop2(S, B, ret):
    k, n = S.get('index'), S.reverse_len
    if 'index' in B and B.get('index') == k:
        return '前一半的元音都和后一半交换过了 → 循环结束'
    pl = S.pos_list
    return (f'第 `{k}` 对：从前数第 {k + 1} 个元音（位置 {pl[k]}）和从后数第 {k + 1} 个元音'
            f'（位置 `pos_list[{n} - {k} - 1] = {pl[n - k - 1]}`）')


def _k(S):
    return S.get('index') if _pair(S) else None


def _k2(S):
    return S['reverse_len'] - S['index'] - 1 if _pair(S) else None


def _cap_swap(S, B, ret):
    k, n, pl = B.index, B.reverse_len, B.pos_list
    a, b = pl[k], pl[n - k - 1]
    return f'交换 `res[{a}]` 和 `res[{b}]`：`"{B.res[a]}"` ↔ `"{B.res[b]}"`'


CONFIG = dict(
    num=345, title='反转字符串中的元音字母', difficulty='Easy', category='双指针',
    author='yiduobo', technique='记录元音位置，前后两两交换',
    tags=['字节30天'],
    code='''
class Solution(object):
    def reverseVowels(self, s):
        pos_list = []
        for index, char in enumerate(s):
            if char in ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']:
                pos_list.append(index)

        reverse_len = len(pos_list)

        res = list(s)
        for index in range(reverse_len//2):
            res[pos_list[index]], res[pos_list[reverse_len - index - 1]] = \\
                res[pos_list[reverse_len - index - 1]], res[pos_list[index]]

        return ''.join(res)
''',
    call=f'Solution().reverseVowels({S0!r})',
    expect='AceCreIm',
    views=[
        dict(type='string', var='s', label='s（紫 = 元音，橙 = 正在检查的字符）', cell=90,
             pointers={_scan: 'orange'}, pointer_labels={_scan: 'index'}, color=_s_color),
        dict(type='array', var='pos_list', label='pos_list（元音的位置）', cell=80,
             pointers={_k: 'cyan', _k2: 'pink'}, pointer_labels={_k: 'index', _k2: 'len-1-index'}),
        dict(type='string', var='res', label='res（粉 = 这一步要交换的两个元音，紫 = 元音位置）', cell=90,
             pointers={_a: 'cyan', _b: 'pink'}, pointer_labels={_a: '前', _b: '后'}, color=_res_color),
    ],
    watch=[('index', 'index', 'orange'), ('char', lambda S: S.get('char') if 'res' not in S else None), ('reverse_len', 'reverse_len', 'cyan')],
    skip=['for index, char in enumerate(s)', 'res[pos_list[reverse_len - index - 1]], res[pos_list[index]]'],
    captions={
        'pos_list = []': '第一步：扫描一遍，把==元音字母的位置==记到 `pos_list`',
        "if char in ['a'": _cap_if,
        'pos_list.append(index)': '`pos_list` = {pos_list}',
        'reverse_len = len(pos_list)': '一共 `{reverse_len}` 个元音，要交换 `{reverse_len} // 2 = {reverse_len // 2}` 对',
        'res = list(s)': 'Python 字符串不可修改 → 先转成列表 `res`',
        'for index in range': _cap_loop2,
        'res[pos_list[index]], res[pos_list[reverse_len - index - 1]] =': _cap_swap,
        "return ''.join(res)": '拼回字符串：=={ret}==',
    },
    cards=dict(
        one_liner='先记下所有元音的位置，再按位置前后两两交换',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['只反转字符串中的==元音字母== `a e i o u`（大小写都算），其余字符不动',
                 '示例：`"IceCreAm"` → `"AceCreIm"`',
                 '示例：`"leetcode"` → `"leotcede"`'],
        quote='比较基础的题目。==记录下字符串中元音字母的位置==，然后根据位置前后两两交换即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`pos_list`：元音在 `s` 里的下标，从小到大',
              '第 `k` 个和倒数第 `k` 个交换：`pos_list[k]` ↔ `pos_list[len - k - 1]`',
              '只换前一半（`len // 2` 对），奇数个时中间那个不动'],
        summary=['时间 `O(n)`，空间 `O(n)`（位置列表 + 字符列表）',
                 '易错：==大写元音也要算==，`"IceCreAm"` 里的 I 和 A',
                 '易错：循环只走 `len // 2` 次，走满会换回去',
                 '也可以直接用左右双指针在 `res` 上相向找元音，省掉 `pos_list`',
                 '原文为 Python 2 写法：`reverse_len/2` 改为 `//`；删去文档字符串，过长的交换语句用 `\\` 折成两行'],
    ),
)
