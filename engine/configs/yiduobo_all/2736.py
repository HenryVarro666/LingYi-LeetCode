def _fmt(v):
    x, y, val = v
    return f'{x},{y}|{val}' if val > 0 else f'Q{-val}:{x},{y}'


def _cap_merge(S, B, r):
    return f'合并区间 `[{S.left}, {S.right}]`：左半 `[{S.left}, {S.mid}]`，右半 `[{S.mid + 1}, {S.right}]`'


def _info_txt(S):
    if 'left' not in S or 'right' not in S:
        return '每个点：数据点 `x,y|和`，询问点 `Qi:x,y`（排序时数值取 -i）'
    s = f'当前合并 [`{S["left"]}`, `{S["right"]}`]'
    if 'ma' in S:
        s += f'　左侧已见数据点的最大和 `ma = {S["ma"]}`'
    return s


def _inrange(S, i, v):
    return 'left' in S and 'right' in S and not (S['left'] <= i <= S['right'])


def _color(S, i, v):
    if v[2] <= 0:
        return 'pink'
    return 'cyan'


def _row(cv, S, box, name, title, ptr, T):
    x0, y0, x1, y1 = box
    arr = S.get(name)
    cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
    if arr is None:
        return
    n = max(len(arr), 1)
    cell = min(150, (x1 - x0 - 40) / max(n, 4))
    sx = x0 + 20
    top = y0 + 48
    L, R = S.get('left'), S.get('right')
    for k, v in enumerate(arr):
        X = sx + k * cell
        isq = v[2] <= 0
        inwin = ptr and L is not None and R is not None and L <= k <= R
        fill = T['pink'] if isq else T['cyan']
        if ptr and L is not None and not inwin:
            fill = (70, 76, 86)
        cv.rect((X + 3, top, X + cell - 3, top + 74), fill=fill, r=8,
                outline=T['yellow'] if inwin else None, width=3 if inwin else 1)
        lab = f'Q{-v[2]}' if isq else f'和{v[2]}'
        cv.text((X + cell / 2, top + 22), lab, 24, T['bg'], anchor='mm', bold=True)
        cv.text((X + cell / 2, top + 54), f'x={v[0]} y={v[1]}', 19, T['bg'], anchor='mm')
        cv.text((X + cell / 2, top + 80), k, 18, T['dim'], anchor='mt', mono=True)
    if ptr:
        for nm, c in (('i', T['blue']), ('j', T['pink'])):
            idx = S.get(nm)
            if idx is not None and 0 <= idx < len(arr):
                X = sx + idx * cell + cell / 2
                cv.tri_up(X, top + 112, 10, c)
                cv.text((X, top + 128), nm, 22, c, anchor='mt', bold=True)


def _draw_info(cv, S, B, box, T):
    _row(cv, S, box, 'info', 'info（青 = 数据点，显示和；粉 = 询问点 Qi；黄框 = 当前合并区间）', True, T)


def _draw_tmp(cv, S, B, box, T):
    _row(cv, S, box, 'tmp', 'tmp（按 y 从大到小归并出的结果）', False, T)


CONFIG = dict(
    num=2736, title='最大和查询', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='按 x 排序 + 按 y 归并（CDQ 分治）',
    tags=['灵神题单·单调栈', '灵神题单·常用数据结构', '难度分 2533'],
    code='''
class Solution(object):
    def maximumSumQueries(self, nums1, nums2, queries):

        info = []
        for x, y in zip(nums1, nums2):
            info.append([x, y, x + y])
        
        for index, (x, y) in enumerate(queries):
            info.append([x, y, -index])
        
        info.sort(key=lambda d:(d[0], d[2]), reverse=True)
        
        res = [-1] * len(queries)

        def merge(info, left, right, res):
            if left == right:
                return
                
            mid = (left + right) // 2

            merge(info, left, mid, res)
            merge(info, mid + 1, right, res)

            i = left
            j = mid + 1
            ma = -1
            tmp = []
            while i <= mid and j <= right:
                if info[i][1] >= info[j][1]:
                    x, y, v = info[i]
                    if v > 0:
                        ma = max(ma, v)
                    i += 1
                    tmp.append([x, y, v])
                else:
                    x, y, v = info[j]
                    if v <= 0:
                        res[-v] = max(res[-v], ma)
                    j += 1
                    tmp.append([x, y, v])
            
            while i <= mid:
                x, y, v = info[i]
                i += 1
                tmp.append([x, y, v])
            
            while j <= right:
                x, y, v = info[j]
                if v <= 0:
                    res[-v] = max(res[-v], ma)
                j += 1
                tmp.append([x, y, v])

            for index in range(len(tmp)):
                info[index + left] = tmp[index][:]

        merge(info, 0, len(info) - 1, res)
        
        return res
''',
    call='Solution().maximumSumQueries([4,2], [3,5], [[3,3],[5,1]])',
    expect=[7, -1],
    max_steps=110,
    skip=['info = []', 'i = left', 'j = mid + 1', 'tmp = []', 'x, y, v = info[', 'i += 1', 'j += 1', 'info[index + left]', 17, 'while i <= mid:', 'while j <= right:', 'for index in range(len(tmp))'],
    views=[
        dict(type='text', fn=_info_txt, size=24),
        dict(type='calls', h=130, hide=('info', 'res')),
        dict(type='custom', draw=_draw_info, h=260),
        dict(type='custom', draw=_draw_tmp, h=150),
        dict(type='array', var='res', label='res', cell=120, h=170,
             color=lambda S, i, v: 'green' if v != -1 else None),
    ],
    watch=['left', 'right', ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ma', 'ma', 'cyan'), ('res', 'res', 'green')],
    captions={
        'info.append([x, y, x + y])': '数据点 `[x, y, x+y]` 加入 info：`{info[-1]}`',
        'info.append([x, y, -index])': '询问点 `[x, y, -{index}]`：数值取 ==-index==，方便排序和定位答案',
        'info.sort': '按 `x` 从大到小排，x 相同时数值大的在前 → ==数据点排在同 x 的询问点前面==：x 这一维已满足',
        'res = [-1]': '`res` 初始全 `-1`',
        'if left == right': lambda S, B, r: ('区间只有一个元素，直接返回' if S.left == S.right else '区间多于一个元素，继续分治'),
        'mid = ': '切成两半：`mid = {mid}`，左 `[{left}, {mid}]`，右 `[{mid + 1}, {right}]`',
        'merge(info, left, mid, res)': '先递归处理左半 `[{left}, {mid}]`',
        'merge(info, mid + 1, right, res)': '再递归处理右半 `[{mid + 1}, {right}]`',
        'ma = -1': '`ma` 记录左半里已经扫过的数据点的最大和，==左半的 x 都 ≥ 右半的 x==',
        'while i <= mid and j <= right': lambda S, B, r: ('左右两半都按 y 从大到小，二路归并' if S.i <= S.mid and S.j <= S.right else '一边用完了，另一边剩下的按序放入 `tmp`（右边剩的询问点仍用 `ma` 更新）'),
        'if info[i][1] >= info[j][1]': lambda S, B, r: (
            f'左 y=`{S.info[S.i][1]}` ≥ 右 y=`{S.info[S.j][1]}` → 左边先出：它的 x 够大、y 也够大，==可以给后面的右侧询问用=='
            if S.info[S.i][1] >= S.info[S.j][1] else
            f'左 y=`{S.info[S.i][1]}` < 右 y=`{S.info[S.j][1]}` → 右边先出，左边剩下的 y 都不够，==不能再更新它=='),
        'if v > 0:': lambda S, B, r: ('是数据点 → 用它的和更新 `ma`' if S.v > 0 else '是询问点 → 左半里的询问不用在这里处理'),
        'ma = max(ma, v)': '`ma` = max({B.ma}, {v}) = =={ma}==',
        'if v <= 0:': lambda S, B, r: (
            f'是询问点 Q{-S.v} → 用 `ma` 更新答案' if S.v <= 0 else '是数据点 → 不用更新答案'),
        'res[-v] = max': '`res[{-v}] = max({B.res[-v]}, ma={ma})` = =={res[-v]}==',
        'tmp.append': '放进 `tmp`：`{tmp[-1]}`',
        'return res': '全部合并完，答案 `{res}`',
    },
    cards=dict(
        one_liner='先按 x 排序，再按 y 做归并：左半的数据点更新右半的询问',
        complexity='时间 `O((n+q) log(n+q))`，空间 `O(n+q)`',
        problem=['两个数组 `nums1`、`nums2`，若干询问 `[x, y]`',
                 '在 `nums1[j] ≥ x` 且 `nums2[j] ≥ y` 的 `j` 中求 `nums1[j]+nums2[j]` 最大值，没有则 `-1`',
                 '本视频：`[4,2]`、`[3,5]`，询问 `[[3,3],[5,1]]` → `[7,-1]`'],
        quote='将所有数据点以及询问点都收集起来……对info以x这一维为第一关键字，数值这一维为第二关键字，从大到小进行排序……再以y坐标为关键字从大到小执行归并排序。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据点和询问点混在一起，按 `x` 降序：询问点前面的数据点 ==x 都够大==',
              '归并时左半的 x ≥ 右半的 x：左半数据点 y ≥ 右半询问 y，就能更新它',
              '二路归并天然按 y 降序，扫到右侧询问时，`ma` 已含所有 y 够大的左侧数据点'],
        summary=['时间 `O((n+q) log(n+q))`，空间 `O(n+q)`',
                 '询问点数值取 `-index`：==数据点排在同 x 询问点之前==，同时能反查答案位置',
                 '左右半区间内部的配对已在递归中处理，不会漏',
                 '原文为 Python 2 写法，`mid = (left + right) / 2` 已改为 `//`',
                 '对比灵神：灵神排序后用单调栈 + 二分；这里用归并（CDQ 分治）'],
    ),
)
