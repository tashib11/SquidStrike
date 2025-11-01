for i in range(len(blue_pieces)):
            if i not in state.dead_blue:
                # Reward advancing forward (lower y value)
           