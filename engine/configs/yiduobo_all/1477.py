def _win(S):
    if 'right' in S and 'left' in S and S['left'] <= S['right']:
        return f"窗口 `arr[{S['left']}..{S['right']}]`，和 `now = {S['now']}`，目标 `{S['target']}`"
    return '滑动窗口（正数数组不需要前缀和）：和超了就收缩 `left`'


CONFIG = dict(
    num=1477, title='找两个和为目标值且不重叠的子数组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='双指针 + 前缀最短长度表',
    tags=['灵神题单·动态规划', '难度分 1851'],
    code='''
class Solution(object):
    def minSumOfLengths(self, arr, target):

        left = 0
        now = arr[0]
        if now == target:
            prev_min = [1]
        else:
            prev_min = [None]
        
        res = None
        for right in range(1, len(arr)):
            now += arr[right]
            while left <= right and now > target:
                now -= arr[left]
                left += 1
            
            prev_min.append(prev_min[-1])
            if now == target:
                if left > 0 and prev_min[left - 1] is not None and (res is None or res > prev_min[left - 1] + right - left + 1):
                    res = prev_min[left - 1] + right - left + 1
                
                if prev_min[-1] is None or prev_min[-1] > right - left + 1:
                    prev_min[-1] = right - left + 1
        
        if res is None:
            res = -1

        return res
''',
    call='Solution().minSumOfLengths([3,1,1,4,1,2,1], 3)',
    expect=3,
    views=[
        dict(type='array', var='arr', label='arr（蓝框 = 当前窗口）', h=190, cell=76,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right')),
        dict(type='array', var='prev_min', label='prev_min[i]：arr[0..i] 内最短合法子数组（None = 无）', h=190, cell=70,
             color=lambda S, i, v: 'yellow' if S.get('_line') in (23, 24) and i == len(S['prev_min']) - 1 else None),
        dict(type='text', fn=_win, size=26, h=80),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'now', ('res', 'res', 'green')],
    captions={
        'left = 0': '双指针 `[left, right]` 维护窗口，`now` 是窗口内的和',
        'prev_min = [1]': '`arr[0] = target`：前缀 `arr[0..0]` 里最短的合法子数组长度是 1',
        'prev_min = [None]': '`arr[0] != target`：前缀 `arr[0..0]` 里还没有合法子数组，记 `None`',
        'res = None': '`res` 保存答案，`None` 表示还没找到两个子数组',
        'for right in range': lambda S, B, ret: ('右端点都走完了，循环结束' if B.get('right') == S.right else f'右端点 `right = {S.right}`'),
        'now += arr[right]': '`now` += `{arr[right]}` → =={now}==',
        'while left <= right': '`now = {now}` {"> target，太大，收缩左端点" if now > target else "<= target，窗口不用再缩"}（`target = {target}`）',
        'now -= arr[left]': '丢掉 `arr[{B.left}] = {arr[B.left]}`：`now` → {now}',
        'left += 1': '`left` → {left}',
        'prev_min.append(prev_min[-1])': '先把前一位的最短长度抄过来：`prev_min[{right}] = {prev_min[-1]}`，如果窗口命中再更新',
        'if now == target': '`now = {now}`，`target = {target}`：{"窗口恰好是一个合法子数组" if now == target else "没有命中，继续右移"}',
        'if left > 0 and': '第二个子数组 `[{left}, {right}]` 之前要有第一个：`prev_min[{left - 1}]` = {prev_min[left - 1] if left > 0 else "不存在"}',
        'res = prev_min': '用 “前面最短 + 当前窗口长度” 更新答案：`res` = =={res}==',
        'if prev_min[-1] is None': '再看当前窗口能否成为 `arr[0..{right}]` 内更短的合法子数组（`prev_min[{right}] = {prev_min[-1]}`）',
        'prev_min[-1] = right': '更新 `prev_min[{right}]` = =={prev_min[-1]}==',
        'if res is None': '`res = {res}`：{"从没凑出两段，要返回 -1" if res is None else "已有答案，直接返回"}',
        'res = -1': '`res = -1`',
        'return res': '最小长度和 `{ret}`',
    },
    cards=dict(
        one_liner='正数数组用双指针找子数组，前缀里最短的那段随手记下',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `arr` 全是正数，在其中找两个==不重叠==的子数组，和都等于 `target`',
                 '返回两个子数组长度和的最小值，找不到返回 `-1`',
                 '示例：`[3,1,1,4,1,2,1], target = 3` → `3`（`[3]` + `[1,2]`）'],
        quote='除此之外，注意到题目这里的arr中都是正数，那么在这里没有必要使用前缀和，而只需要使用双指针来求解和等于target的子数组。',
        quote_src='—— yiduobo 题解原文',
        idea=['一般子数组问题用前缀和：当前前缀和 `s`，找之前出现过的 `s - target`',
              '本题全是正数，双指针 `[left, right]` 维护和，更省事',
              '`prev_min[i]` 记 `arr[0..i]` 里最短的合法子数组；窗口命中时用 `prev_min[left-1]` 更新答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`prev_min` 要先 `append` 前一位的值，命中后再改小，才能保证长度对齐',
                 '易错：用的是 `prev_min[left - 1]`，保证两个子数组不重叠',
                 '`res` 和 `prev_min` 的 `None` 表示“不存在”，要先判断再比较',
                 '原文为 Python 2 写法，仅删去了类型说明文档字符串（本份代码无需其他修改）'],
    ),
)
