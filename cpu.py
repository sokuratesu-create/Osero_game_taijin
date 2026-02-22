import random

def cpu_get_move(board, player):
    from app import get_flip_stone, board_size
    put_stones = []

    for r in range(board_size):
        for c in range(board_size):
            stones = get_flip_stone(r, c, player, board)
            if len(stones) > 0:
                put_stones.append((r, c))
    
    if put_stones:
        #ランダムに置く場所を選択
        choice_stone = random.choice(put_stones)
        return choice_stone
    
    return None