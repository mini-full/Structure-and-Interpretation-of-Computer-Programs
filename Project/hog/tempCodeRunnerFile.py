
        def strategy_for(player):
            def strategy(*scores):
                nonlocal final_scores, move_cnt, who
                final_scores = scores
                if player:
                    final_scores = final_scores[::-1]
                who = player
                if move_cnt == len(move_history):
                    raise HogLoggingException()
                move = move_hist