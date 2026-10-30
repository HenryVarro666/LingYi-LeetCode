def _mt(S):
    if 'res' in S and 'left' in S and 'right' in S and S['_line'] >= 21 and 'index' in S:
        i = S['index']
        if S['left'][i] > 1 and S['right'][i] > 1:
            return f"以下标 `{i}` 为山顶：`{S['left'][i]} + {S['right'][i]} − 1` = =={S['left'][i]+S['right'][i]-1}=="
        return f"下标 `{i}`：`left = {S['left'][i]}`，`right = {S['right'][i]}`，有一边为 1，不能当山顶"
    return ''


CONFIG = dict(
    num=845, title='数组中的最长山脉', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='正反两趟预处理 + 枚举山顶',
    tags=['动态规划'],
    code='''
class Solution(object):
    def longestMountain(self, arr):

        if len(arr) < 3:
            return 0
        
        left = [1]
        for index in range(1, len(arr)):
            if arr[index] > arr[index - 1]:
                left.append(left[-1] + 1)
            else:
                left.append(1)
        
        right = [1]
        for index in range(len(arr) - 2, -1, -1):
            if arr[index] > arr[index + 1]:
                right.append(right[-1] + 1)
            else:
                right.append(1)
        right.reverse()

        res = 0
        for index in range(len(arr)):
            if left[index] > 1 and right[index] > 1:
                res = max(res, left[index] + right[index] - 1)
        
        return res
''',
    call='Solution().longestMountain([2,1,4,7,3,2,5])',
    expect=5,
    views=[
        dict(type='bars', var='arr', h=300, pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='array', var='left', h=140, label='left：以 arr[i] 结尾的连续上升长度', pointers={'index': 'blue'}),
        dict(type='array', var='right', h=140, label='right：以 arr[i] 开头的连续下降长度', pointers={'index': 'pink'}),
        dict(type='text', fn=_mt),
    ],
    watch=['index', ('res', 'res', 'green')],
    captions={
        'len(arr) < 3': '山脉至少 3 个元素，太短直接返回 0',
        'left = [1]': '`left[i]`：以 `arr[i]` 结尾的严格上升段长度，`left[0] = 1`',
        'for index in range(1, len': lambda S, B, r: ('遍历完毕，循环结束' if B.get('index') == S['index'] else f'从左往右：`index = {S["index"]}`'),
        'for index in range(len(arr) - 2': lambda S, B, r: ('遍历完毕，循环结束' if B.get('index') == S['index'] else f'从右往左：`index = {S["index"]}`'),
        'for index in range(len(arr)):': '枚举山顶：`index = {index}`',
        'if arr[index] > arr[index - 1]': '`arr[{index}] = {arr[index]}` 与前一个 `{arr[index-1]}`：{"更大，上升段可以延长" if arr[index] > arr[index-1] else "不更大，上升段断开，重新从 1 开始"}',
        'left.append(left[-1] + 1)': '上升延续：`left[{index}]` = `{left[-1]}`',
        'left.append(1)': '上升断开：`left[{index}]` = 1',
        'right = [1]': '从右往左扫：`right[i]` 是以 `arr[i]` 开头的严格下降段长度',
        'if arr[index] > arr[index + 1]': '`arr[{index}] = {arr[index]}` 与后一个 `{arr[index+1]}`：{"更大，下降段延长" if arr[index] > arr[index+1] else "不更大，下降段断开"}',
        'right.append(right[-1] + 1)': '下降延续：追加 `{right[-1]}`（此时 right 是倒着存的）',
        'right.append(1)': '下降断开：追加 1',
        'right.reverse()': '倒着存的，翻转后下标就和 `arr` 对齐了',
        'res = 0': '`res` 记录最长山脉',
        'if left[index] > 1 and right[index] > 1': '山顶左右都得有坡：`left = {left[index]}`，`right = {right[index]}` → {"满足" if left[index] > 1 and right[index] > 1 else "不满足"}',
        'res = max': '山脉长度 `left + right − 1`（山顶只算一次）：`res` = =={res}==',
        'return res': '最长山脉长度 ==`{res}`==',
    },
    cards=dict(
        one_liner='预处理每个点向左的上升长度和向右的下降长度',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['山脉：先严格上升再严格下降，长度至少 3，峰顶两侧都得有坡',
                 '求 `arr` 中最长的山脉子数组长度，没有则返回 0',
                 '本视频：`[2,1,4,7,3,2,5]` → `5`（`1,4,7,3,2`）'],
        quote='left[index]表示以arr[index]为终点的单调递增子数组的长度，而right[index]则表示以arr[index]为起点的单调递减子数组的长度，这两个数组可以通过正反两趟扫描求得。',
        quote_src='—— yiduobo 题解原文',
        idea=['正着扫得 `left`，倒着扫得 `right`',
              '枚举山顶：`left > 1` 且 `right > 1` 才有山脉',
              '山脉长度 = `left + right − 1`，取最大'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '==山顶要减 1==：左右坡都把山顶算进去了',
                 '用严格大于：平台（相等）会断开上升/下降段',
                 '`right` 是倒着 append 的，别忘了 `reverse()`'],
    ),
)
