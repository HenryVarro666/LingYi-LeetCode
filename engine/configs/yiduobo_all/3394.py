def _cur(S):
    try:
        l = S['index_list']
        return l.index((S['now_start'], S['now_end']))
    except Exception:
        return None


def _out(S):
    if 'start' in S and 'end' in S:
        return [[S['start'], S['end']]]
    return []


class _V:
    def __init__(self, fn, name):
        self.fn, self.name = fn, name

    def __call__(self, S):
        return self.fn(S)

    def __str__(self):
        return self.name


def _txt(S):
    if 'cnt' not in S:
        return '横纵坐标互相独立：分别把 x 投影、y 投影当成区间，合并后数个数'
    ax = '竖切（x 区间）' if S.get('index_list') is S.get('x_list') else '横切（y 区间）'
    return f'{ax}　已合并出 `cnt = {S["cnt"]}` 段，当前合并区间 `[{S["start"]}, {S["end"]}]`'


def _if(S, B, ret):
    ns, e = B.now_start, B.end
    if ns < e:
        return f'`now_start = {ns} < end = {e}`：==相交==，合并，只更新终点'
    return f'`now_start = {ns} ≥ end = {e}`：==不相交==，上一段定型，新开一段'


CONFIG = dict(
    num=3394, title='判断网格图能否被切割成块', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='x/y 分别合并区间，段数 ≥ 3',
    tags=['灵神题单', '贪心算法', '难度分 1916'],
    code='''
class Solution(object):
    def checkValidCuts(self, n, rectangles):
        
        x_list = []
        y_list = []
        for x1, y1, x2, y2 in rectangles:
            x_list.append((x1, x2))
            y_list.append((y1, y2))
        
        def check(index_list):
            index_list.sort()
            start, end = index_list[0]
            cnt = 1

            for now_start, now_end in index_list[1:]:
                if now_start < end:
                    end = max(end, now_end)
                else:
                    cnt += 1
                    start, end = now_start, now_end

            return cnt >= 3

        return check(x_list) or check(y_list)
''',
    call='Solution().checkValidCuts(5, [[1,0,5,2],[0,2,2,4],[3,2,5,3],[0,4,4,5]])',
    expect=True,
    views=[
        dict(type='text', fn=_txt, size=24),
        dict(type='intervals', var='index_list', out=_V(_out, '当前合并区间 [start, end]'), pointer=_cur,
             label='投影区间（蓝，黄 = 当前）与正在合并的区间（绿）', h=430),
    ],
    watch=[('cnt', 'cnt', 'green'), ('start', 'start', 'blue'), ('end', 'end', 'pink'), ('now_start', 'now_start', 'yellow'), ('now_end', 'now_end', 'orange')],
    captions={
        'x_list = []': '`x_list` 放每个矩形的横向投影 `(x1, x2)`',
        'y_list = []': '`y_list` 放纵向投影 `(y1, y2)`',
        'for x1, y1, x2, y2': lambda S, B, rt: ('拆出矩形 `[{}, {}, {}, {}]`'.format(S.x1, S.y1, S.x2, S.y2) if 'x1' not in B or (B.x1, B.y1, B.x2, B.y2) != (S.x1, S.y1, S.x2, S.y2) else '矩形都处理完了：横纵投影都收集好了'),
        'x_list.append': '横向投影加入：`{x_list}`',
        'y_list.append': '纵向投影加入：`{y_list}`',
        'def check': '定义 `check`：给一组区间，判断合并后是否 ≥ 3 段',
        'index_list.sort()': '按起点排序：`{index_list}`',
        'start, end = index_list[0]': '第一个区间 `[{start}, {end}]` 作为当前合并区间',
        'cnt = 1': '已经有 1 段了',
        'for now_start': lambda S, B, rt: ('看下一个区间 `[{}, {}]`'.format(S.now_start, S.now_end) if 'now_start' not in B or B.now_start != S.now_start or B.now_end != S.now_end else '区间都看完了'),
        'if now_start < end': _if,
        'end = max': '终点取大：`end = max({B.end}, {now_end}) = {end}`',
        'cnt += 1': '多出一段：`cnt` → =={cnt}==',
        'start, end = now_start': '新的合并区间 `[{start}, {end}]`',
        'return cnt >= 3': '`cnt = {cnt}`，`≥ 3` 吗 → =={ret}==',
        'return check(x_list)': lambda S, B, rt: ('先看竖切 `check(x_list)`，不行再看横切 `check(y_list)`' if rt is None else '竖切、横切有一个行就行 → 返回 =={}=='.format(rt)),
    },
    cards=dict(
        one_liner='横纵坐标互相独立：x、y 各合并一次区间，有 3 段以上就能切',
        complexity='时间 `O(m log m)`，空间 `O(m)`',
        problem=['`n×n` 网格里有若干不重叠矩形 `[x1,y1,x2,y2]`',
                 '要找两条==同为水平或同为垂直==的线，切出 3 块',
                 '每块至少一个矩形，每个矩形只属于一块',
                 '示例：`n=5`，`[[1,0,5,2],[0,2,2,4],[3,2,5,3],[0,4,4,5]]` → `true`'],
        quote='题目中的横纵坐标是互相独立的，于是可以根据所有矩形的横坐标来判断能否找出合法的垂直分割线，同时根据所有矩形的纵坐标来判断能否找出合法的水平分割线。',
        quote_src='—— yiduobo 题解原文',
        idea=['问题转化成：线段上有若干区间，找两个分割点切成 3 部分',
              '每个区间只能属于一部分 → 相交区间必须合并',
              '排序后一趟遍历合并，合并完区间数 `>= 3` 就能找到分割点'],
        summary=['时间 `O(m log m)`，空间 `O(m)`',
                 '合并条件是 `now_start < end`：首尾相接（`==`）不合并，因为切线可以落在公共端点',
                 '`cnt` 从 1 开始（第一个区间已经算一段）',
                 '`n` 没有用到；`check` 里的 `start` 其实只是跟着记录，不影响计数',
                 '对比灵神：灵神 `cnt` 从 0、`max_r` 从 0 起，把第一个区间也当「新区间」'],
    ),
)
