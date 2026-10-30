



# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# 自顶向下「递」

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        ans = inf
        def dfs(node,cnt):
            if node is None:
                return
                # return
                # return None
                # # 或者函数走到结尾
                # 都等价于： return None    
            cnt += 1
            if node.left is None and node.right is None:
                nonlocal ans
                ans = min(ans, cnt)
                return
            dfs(node.left, cnt)
            dfs(node.right, cnt)
        dfs(root, 0)
        return ans if root else 0
        # if root: # 等价于 if root is not None:
        #     return ans
        # else:
        #     return 0



class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        ans = inf
        def dfs(node, cnt):
            if node is None:
                return
            nonlocal ans
            cnt += 1
            if cnt >= ans:
                return   # 最优性剪枝
            if node.left is None and node. right is None:
                ans = cnt
                return
            dfs(node.left, cnt)
            dfs(node.right, cnt)
        dfs(root, 0)
        return ans if root else 0


# 自底向上「归」
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        if root.right is None:
            return self.minDepth(root.left) + 1
        if root.left is None:
            return self. minDepth(root.right) + 1
        return min(self.minDepth(root.left), self.minDepth(root.right)) + 1