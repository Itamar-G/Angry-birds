import numpy as np
import torch
class State:
    def __init__(self, max_pigs=5, max_blocks=20):
        self.max_pigs = max_pigs
        self.max_blocks = max_blocks
    
    def build(self, env):
        state_list = []
        # -----------------------------
        # 2. Pigs state – each pig: (x, y, vx, vy)
        # -----------------------------
        pig_list = list(env.pigs)
        state_list.append(env.tries)
        for pig in pig_list[:self.max_pigs]:
            state_list += [
                pig.rect.centerx,
                pig.rect.centery,
            ]

        # Fill remaining pigs
        for _ in range(self.max_pigs - len(pig_list)):
            state_list += [0, 0]

        # -----------------------------
        # 3. Blocks state – each block: (x, y, vx, vy, angle, hit)
        # -----------------------------
        block_list = list(env.blocks)

        for block in block_list[:self.max_blocks]:
            state_list += [
                block.rect.bottomleft[0],
                block.rect.bottomleft[1],
                block.rect.width,           # ← רוחב
                block.rect.height,
                block.angle,
                block.hit
            ]
        
        # Fill remaining blocks
        for _ in range(self.max_blocks - len(block_list)):
            state_list += [0, 0, 0, 0, 0, 0]
        return state_list
    def toTensor (self,env, device = torch.device('cpu')):
        state_list = np.array(self.build(env), dtype=np.float32)
        tensor = torch.from_numpy(state_list)
        return tensor
    [staticmethod]
    def tensor_to_state_list(state_tensor):
        if state_tensor.is_cuda:
            state_tensor = state_tensor.cpu()
        return state_tensor.detach().numpy().tolist()