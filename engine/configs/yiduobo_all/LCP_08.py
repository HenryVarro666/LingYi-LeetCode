INC = [[2, 8, 4], [2, 5, 0], [10, 9, 8]]
REQ = [[15, 10, 7], [2, 11, 3]]


def _cur(S):
    """the prefix array currently searched (inner frame f), else None"""
    I = S['_inner']
    return I.get('f') if 'f' in I else None


def _arr_color(name):
    def c(S, i, v):
        f = _cur(S)
        if f is None or f is not S.get(name):
            return None
        I = S['_inner']
        if 'l' in I and 'r' in I:
            if i < I['l']:
                return 'red'
            if i >= I['r'] and I['v'] <= f[-1]:
                return 'green'
        return None
    return c


def _dim(name):
    def d(S, i, v):
        f = _cur(S)
        return f is not None and f is not S.get(name)
    return d


def _ptr(name, var):
    return f"_inner['{var}'] if '{var}' in _inner and _inner.get('f') is {name} else None"


def _top(S):
    I = S['_inner']
    if 'f' in I:
        v = I['v']
        return f'在前缀和里找==第一天== `>= {v}`：红 = 还不够，绿 = 已达到'
    if 'require' in S:
        return f"剧情条件 `{S['require']}`：三个属性各自独立，分别二分"
    return '先算出每一天三种属性的累计值（单调不减）'


def _search_if(S, B, ret):
    I = S['_inner']
    f, v = I['f'], I['v']
    if v > f[-1]:
        return f'`{v} > {f[-1]}`：最后一天都达不到 → 返回 -1'
    return f'`{v} <= {f[-1]}`：最终能达到 → 二分第几天达到'


def _mid_if(S, B, ret):
    I = S['_inner']
    f, m, v = I['f'], I['mid'], I['v']
    if f[m] < v:
        return f'`mid = {m}`，第 {m} 天 `{f[m]} < {v}`：还不够 → 答案在后面，`l = mid + 1`'
    return f'`mid = {m}`，第 {m} 天 `{f[m]} >= {v}`：已达到 → 答案 `<= {m}`，`r = mid`'


def _check(S, B, ret):
    a, b, c = S.date_r, S.date_c, S.date_h
    if a < 0 or b < 0 or c < 0:
        return f'三个天数 `({a}, {b}, {c})` 有 -1：某个属性永远达不到 → 无法触发'
    return f'三个天数 `({a}, {b}, {c})` 都有效 → 三者都要满足，取最大'


CONFIG = dict(
    num='LCP 08', title='剧情触发时间', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='前缀和 + 二分查找',
    tags=['灵神核心路线', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def getTriggerTime(self, increase, requirements):

        tot_r = [0]
        tot_c = [0]
        tot_h = [0]
        for inc in increase:
            tot_r.append(tot_r[-1] + inc[0])
            tot_c.append(tot_c[-1] + inc[1])
            tot_h.append(tot_h[-1] + inc[2])
        
        def search(f, v):
            if v > f[-1]:
                return -1
            l = 0
            r = len(f) - 1
            while l < r:
                mid = (l + r) // 2
                if f[mid] < v:
                    l = mid + 1
                else:
                    r = mid
            
            return l

        res = []
        for require in requirements:
            date_r = search(tot_r, require[0])
            date_c = search(tot_c, require[1])
            date_h = search(tot_h, require[2])
            if date_r < 0 or date_c < 0 or date_h < 0:
                res.append(-1)
            else:
                res.append(max(date_r, date_c, date_h))
                
        return res
''',
    call=f'Solution().getTriggerTime({INC}, {REQ})',
    expect=[-1, 2],
    views=[
        dict(type='text', fn=_top, size=26, h=60),
        dict(type='array', var='tot_r', label='tot_r：第 i 天的属性 0（C）累计值', cell=80, color=_arr_color('tot_r'), dim=_dim('tot_r'),
             pointers={_ptr('tot_r', 'l'): 'blue', _ptr('tot_r', 'mid'): 'yellow', _ptr('tot_r', 'r'): 'pink'},
             pointer_labels={_ptr('tot_r', 'l'): 'l', _ptr('tot_r', 'mid'): 'mid', _ptr('tot_r', 'r'): 'r'}, h=175),
        dict(type='array', var='tot_c', label='tot_c：属性 1（R）累计值', cell=80, color=_arr_color('tot_c'), dim=_dim('tot_c'),
             pointers={_ptr('tot_c', 'l'): 'blue', _ptr('tot_c', 'mid'): 'yellow', _ptr('tot_c', 'r'): 'pink'},
             pointer_labels={_ptr('tot_c', 'l'): 'l', _ptr('tot_c', 'mid'): 'mid', _ptr('tot_c', 'r'): 'r'}, h=175),
        dict(type='array', var='tot_h', label='tot_h：属性 2（H）累计值', cell=80, color=_arr_color('tot_h'), dim=_dim('tot_h'),
             pointers={_ptr('tot_h', 'l'): 'blue', _ptr('tot_h', 'mid'): 'yellow', _ptr('tot_h', 'r'): 'pink'},
             pointer_labels={_ptr('tot_h', 'l'): 'l', _ptr('tot_h', 'mid'): 'mid', _ptr('tot_h', 'r'): 'r'}, h=175),
    ],
    watch=[('require', 'require', 'cyan'), 
           ('date_r', 'date_r'), ('date_c', 'date_c'), ('date_h', 'date_h'), ('res', 'res', 'green')],
    skip=['tot_c = [0]', 'tot_h = [0]', 'res = []', 'l = 0', 'mid = (l + r) // 2', 'l = mid + 1', 'r = mid'],
    max_steps=70,
    captions={
        'tot_r = [0]': '第 0 天三种属性都是 0：三个前缀和数组都从 `[0]` 开始',
        'tot_r.append': '`tot_r` 末尾加 `{inc[0]}` → `{tot_r[-1]}`',
        'tot_c.append': '`tot_c` 末尾加 `{inc[1]}` → `{tot_c[-1]}`',
        'tot_h.append': '`tot_h` 末尾加 `{inc[2]}` → `{tot_h[-1]}`；increase 非负 → ==单调不减==',
        'def search': '`search(f, v)`：在单调数组 `f` 里找第一个 `>= v` 的下标',
        'if v > f[-1]': _search_if,
        'return -1': '返回 -1',
        'r = len(f) - 1': '二分区间 `[l, r] = [0, {r}]`：第 0 天到最后一天',
        'while l < r': lambda S, B, ret: ('`l < r` → 继续二分' if S.l < S.r else f'`l = r = {S.l}`：第 {S.l} 天首次达到'),
        'mid = (l + r) // 2': '`mid = ({l} + {r}) // 2 = {mid}`',
        'if f[mid] < v': _mid_if,
        'l = mid + 1': '`l` → {l}',
        'r = mid': '`r` → {r}',
        'return l': '返回第 =={ret}== 天',
        'for require in requirements': lambda S, B, ret: (f'下一个剧情条件 `{S.require}`' if S.get('require') != B.get('require') else '所有剧情处理完毕'),
        'date_r = search': '属性 0 要 `>= {require[0]}`：去 `tot_r` 里二分最早的一天',
        'date_c = search': '属性 1 要 `>= {require[1]}`：去 `tot_c` 里二分最早的一天',
        'date_h = search': '属性 2 要 `>= {require[2]}`：去 `tot_h` 里二分最早的一天',
        'if date_r < 0': _check,
        'res.append(-1)': '这个剧情无法触发 → `res` 加入 -1',
        'res.append(max': '触发时间 = `max({date_r}, {date_c}, {date_h})` = =={res[-1]}==',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='三种属性互不影响：各自二分出最早达标的一天，再取最大',
        complexity='时间 `O(n + m log n)`，空间 `O(n)`',
        problem=['三种属性初始为 0，第 `i+1` 天三种属性分别增加 `increase[i]`',
                 '剧情 `j` 在三种属性都 `>=` `requirements[j]` 时立刻触发，求每个剧情的触发天数，永远不触发返回 -1',
                 '示例：`increase = [[2,8,4],[2,5,0],[10,9,8]]`',
                 '`requirements = [[2,11,3],[15,10,7],[9,17,12],[8,1,14]]` → `[2,-1,3,-1]`',
                 '本视频取其中两个剧情：`[[15,10,7],[2,11,3]]` → `[-1,2]`'],
        quote='注意到题目给出的increase数组中的值都非负，也就意味着C、R、H这三个属性值是随着日期==单调不减==的。于是可以先将每一天的属性值都计算出来，然后就可以通过二分查找……',
        quote_src='—— yiduobo 题解原文',
        idea=['三种属性互不影响 → 拆开算，每种求「第几天 `>= v`」',
              '前缀和：`tot[i]` = 第 `i` 天的属性值；非负增量 → 单调 → 可以二分',
              '任一属性最终都达不到 → -1；否则三个天数取最大'],
        summary=['时间 `O(n + m log n)`：前缀和 `O(n)`，每个剧情三次二分',
                 '前缀和从 `[0]` 开始，第 0 天要求全 0 的剧情能当天触发',
                 '先判 `v > f[-1]`：最终都达不到就直接 -1，二分区间才保证有解',
                 '原文为 Python 2 写法，`mid = (l + r) / 2` 已改为 `//`'],
    ),
)
