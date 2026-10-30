TREE = [0, 1, 6, 6, 4, 4, 6]
TYPE_COL = {0: 'cyan', 1: 'blue', 6: 'pink', 4: 'orange'}


def _baskets(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    d = S.get('num_dict')
    cv.text((x0 + 18, y0 + 4), 'num_dict = 篮子：每种数字一个篮子，只有 2 个篮子', 22, T['muted'], bold=True)
    if d is None:
        return
    bd = B.get('num_dict') or {}
    items = list(d.items())
    bw, gap = 210, 40
    total = 3 * bw + 2 * gap
    sx = x0 + (x1 - x0 - total) / 2
    top, bot = y0 + 50, y1 - 16
    for k in range(3):
        X = sx + k * (bw + gap)
        extra = k == 2
        if k < len(items):
            key, v = items[k]
            c = T[TYPE_COL.get(key, 'green')]
            changed = key not in bd or bd[key] != v
            cv.rect((X, top, X + bw, bot), fill=T['panel2'], outline=T['red'] if extra else (T['yellow'] if changed else T['border']),
                    width=4 if (extra or changed) else 2, r=16)
            cv.d.ellipse((X + 18, top + 18, X + 74, top + 74), fill=c)
            cv.text((X + 46, top + 46), key, 30, T['bg'], anchor='mm', bold=True)
            cv.text((X + 90, top + 46), f'× {v}', 34, T['text'], anchor='lm', bold=True)
            if extra:
                cv.text((X + bw / 2, bot - 22), '第 3 种：超出！', 24, T['red'], anchor='mm', bold=True)
        else:
            cv.rect((X, top, X + bw, bot), fill=T['panel'], outline=T['red'] if extra else T['border'], width=2, r=16)
            cv.text((X + bw / 2, (top + bot) / 2), '（不允许）' if extra else '空篮子', 22, T['dim'], anchor='mm')


def _cap_add(S, B, ret):
    return f'把 `tree[{S.index}] = {S.num}` 加入窗口 → `num_dict[{S.num}] = {S.num_dict[S.num]}`'


def _cap_while(S, B, ret):
    k = len(S.num_dict)
    if k > 2:
        return f'dict 里有 `{k}` 种数字 > 2 → 将左边界==向右移动=='
    return f'`{k}` 种 ≤ 2，窗口合法'


CONFIG = dict(
    num=904, title='水果成篮', difficulty='Medium', category='滑动窗口',
    author='yiduobo', technique='滑动窗口 + dict 计数',
    tags=['字节30天'],
    code='''
class Solution(object):
    def totalFruit(self, tree):
        num_dict = {}
        res = 0
        l = 0
        for index, num in enumerate(tree):
            num_dict[num] = num_dict.get(num, 0) + 1
            while len(num_dict) > 2:
                num_dict[tree[l]] -= 1
                if num_dict[tree[l]] == 0:
                    num_dict.pop(tree[l])
                l += 1

            res = max(res, index - l + 1)

        return res
''',
    call=f'Solution().totalFruit({TREE})',
    expect=5,
    skip=['for index, num in'],
    views=[
        dict(type='array', var='tree', label='tree（框 = 滑动窗口 [l, index]）', cell=104,
             pointers={'l': 'blue', 'index': 'pink'}, pointer_labels={'l': 'l(左)'}, window=('l', 'index'),
             color=lambda S, i, v: TYPE_COL.get(v),
             dim=lambda S, i, v: 'index' in S and not (S['l'] <= i <= S['index']), h=250),
        dict(type='custom', draw=_baskets, h=230),
        dict(type='text', fn=lambda S: (f"窗口长度 `index − l + 1 = {S['index'] - S['l'] + 1}`，`res = {S['res']}`"
                                        if 'index' in S else ''), h=56),
    ],
    watch=[('l', 'l', 'blue'), ('index', 'index', 'pink'), 'num', ('res', 'res', 'green')],
    captions={
        'num_dict = {}': '`num_dict`：当前窗口中==每种数字出现的个数==',
        'res = 0': '`res` 记录答案',
        'l = 0': '`l` 是滑动窗口的左边界',
        'num_dict[num] = ': _cap_add,
        'while len(num_dict) > 2': _cap_while,
        'num_dict[tree[l]] -= 1': '左边界的 `tree[{l}] = {tree[l]}` 移出窗口 → 个数变为 `{num_dict[tree[l]]}`',
        'if num_dict[tree[l]] == 0': lambda S, B, r: (f'`{S.tree[S.l]}` 的个数为 0' if S.num_dict[S.tree[S.l]] == 0
                                                      else f'`{S.tree[S.l]}` 还剩 `{S.num_dict[S.tree[S.l]]}` 个'),
        'num_dict.pop': '把 `{B.tree[l]}` 从 dict 中==弹出==：篮子腾出来了',
        'l += 1': '左边界 `l` → {l}',
        'res = max': '调整完左边界，窗口 `[{l}, {index}]` 长 `{index - l + 1}` → `res = {res}`',
        'return res': '最长的、只含两种数字的连续子序列长 =={ret}==',
    },
    cards=dict(
        one_liner='最多两种数字的最长连续子数组：dict 计数 + 滑动窗口',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一排果树，`tree[i]` 是第 `i` 棵树的水果==种类==；只有两个篮子，每个只装一种',
                 '从任意一棵树开始向右，每棵树摘一个；遇到装不下的种类就停',
                 '示例：`[1,2,1]` → `3`；`[1,2,3,2,2]` → `4`',
                 f'本视频：`{TREE}` → `5`'],
        quote='若此时dict中不同数字个数超过2个，那么就将滑动窗口的左边界向右移动，同时将对应的数字从dict中弹出，==直到dict中不同数字的个数小于等于2==。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目即：找最长的连续子序列，==最多只包含两种==不同数字',
              '用 dict 维护窗口中每种数字的个数，从头到尾一趟扫描',
              '超过 2 种就右移左边界、减计数，个数为 0 时弹出；调整完再更新答案'],
        result='`res = 5`：窗口 `[2, 6]` = `[6,6,4,4,6]`',
        summary=['时间 `O(n)`：左右边界都只往右走；空间 `O(1)`（dict 至多 3 个键）',
                 '易错：个数减到 0 要 `pop`，否则 `len(num_dict)` 偏大',
                 '`num_dict.get(num, 0) + 1`：普通 dict 的计数写法',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串；参数名 `tree` 照原文保留',
                 '对比灵神：同为滑动窗口，灵神用 `defaultdict` 和 `out` 变量更紧凑'],
    ),
)
