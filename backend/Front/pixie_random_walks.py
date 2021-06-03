import time
import math
import random
import numpy as np
from tqdm import tqdm


def generate_board_to_pin(userNum, paperNum):
    board_to_pin = dict()
    for userid in tqdm(range(userNum)):
        board_to_pin[userid] = []
        tmp = random.randint(30, 100)
        for i in range(tmp):
            board_to_pin[userid].append(
                (
                    random.randint(0, paperNum-1),
                    math.ceil(34 / (random.randint(0, 59) + 6))
                )
            )
    return board_to_pin


def generate_pin_to_board(board_to_pin):
    pin_to_board = dict()
    for userid in tqdm(board_to_pin):
        for paperid, ttt in board_to_pin[userid]:
            if paperid in pin_to_board:
                pin_to_board[paperid].append((userid, ttt))
            else:
                pin_to_board[paperid] = [(userid, ttt)]
    return pin_to_board


def weight(ttt):
    if ttt > 28:
        return 1
    if ttt > 14:
        return 2
    if ttt > 7:
        return 3
    if ttt > 3:
        return 4
    return 5


def random_by_prob(prob):
    return np.argmax(np.random.multinomial(1, prob, size=1))


def random_walk_according_to_time(adj_list, idx, cache, current_date):
    if idx in cache:
        return cache[idx][random.randint(0, len(cache[idx])-1)]
    candidate_pool = []
    for cand_idx, ttt in adj_list[idx]:
        # candidate_pool += [cand_idx] * weight(ttt)
        timegap = (current_date - ttt).days + 5
        candidate_pool += [cand_idx] * math.ceil(34 / timegap)
    cache[idx] = candidate_pool
    return candidate_pool[random.randint(0, len(candidate_pool)-1)]


def random_walk_according_to_time_new(adj_list, idx, cache, current_date):
    if idx in cache:
        return adj_list[idx][random_by_prob(cache[idx])][0]
    prob = []
    for cand in adj_list[idx]:
        timegap = (current_date - cand[1]).days + 5
        prob.append(math.ceil(34 / timegap))
    prob = np.array(prob) / np.sum(prob)
    cache[idx] = prob
    return adj_list[idx][random_by_prob(prob)][0]


def pixie_random_walk(
    board_to_pin, pin_to_board, cache_user_candidates,
    cache_paper_candidates, userid, chosen_paper_num,
    chosen_author_num, current_date,
    alpha=0.5, threshold_paper=10, threshold_author=80
):
    userboard = set([tpl[0] for tpl in board_to_pin[userid]])
    chosen_paper = set()
    count_paper = dict()
    chosen_author = set()
    count_author = dict()
    epoch = 0
    while len(chosen_paper) < chosen_paper_num or \
            len(chosen_author) < chosen_author_num:
        # print(epoch, len(chosen_paper), len(chosen_author))
        epoch += 1
        curpaperid = random_walk_according_to_time(
            board_to_pin, userid, cache_user_candidates, current_date)
        while True:
            curuserid = random_walk_according_to_time(
                pin_to_board, curpaperid, cache_paper_candidates, current_date)
            if curuserid != userid:
                if curuserid in count_author:
                    count_author[curuserid] += 1
                    if count_author[curuserid] >= threshold_author and\
                            curuserid not in chosen_author:
                        chosen_author.add(curuserid)
                else:
                    count_author[curuserid] = 1

            curpaperid = random_walk_according_to_time(
                board_to_pin, curuserid, cache_user_candidates, current_date)
            if curpaperid not in userboard:
                if curpaperid in count_paper:
                    count_paper[curpaperid] += 1
                    if count_paper[curpaperid] >= threshold_paper and\
                            curpaperid not in chosen_paper:
                        chosen_paper.add(curpaperid)
                else:
                    count_paper[curpaperid] = 1
            if random.random() < alpha:
                break

    return sorted(
        [(paperid, count_paper[paperid]) for paperid in chosen_paper],
        key=lambda x: x[1], reverse=True
    ), sorted(
        [(authorid, count_author[authorid])for authorid in chosen_author],
        key=lambda x: x[1], reverse=True
    )


def pixie_random_walk_only_paper(
    board_to_pin, pin_to_board, cache_user_candidates, cache_paper_candidates,
    userid, chosen_paper_num, current_date, alpha=0.5, threshold_paper=10,
    max_epoch=100000
):
    userboard = set([tpl[0] for tpl in board_to_pin[userid]])
    chosen_paper = set()
    count_paper = dict()
    epoch = 0
    while len(chosen_paper) < chosen_paper_num and epoch < max_epoch:
        # print(epoch, len(chosen_paper), len(chosen_author))
        epoch += 1
        curpaperid = random_walk_according_to_time(
            board_to_pin, userid, cache_user_candidates, current_date)
        while True:
            curuserid = random_walk_according_to_time(
                pin_to_board, curpaperid, cache_paper_candidates, current_date)
            curpaperid = random_walk_according_to_time(
                board_to_pin, curuserid, cache_user_candidates, current_date)
            if curpaperid not in userboard:
                if curpaperid in count_paper:
                    count_paper[curpaperid] += 1
                    if count_paper[curpaperid] >= threshold_paper:
                        chosen_paper.add(curpaperid)
                else:
                    count_paper[curpaperid] = 1
            if random.random() < alpha:
                break

    return sorted(
        [(paperid, count_paper[paperid]) for paperid in chosen_paper],
        key=lambda x: x[1], reverse=True
    )


def pixie_random_walk_only_author(
    board_to_pin, pin_to_board, cache_user_candidates,
    cache_paper_candidates, userid, chosen_author_num,
    current_date, alpha=0.5, threshold_author=50,
    max_epoch=10000
):
    userboard = set([tpl[0] for tpl in board_to_pin[userid]])
    chosen_author = set()
    count_author = dict()
    epoch = 0
    while len(chosen_author) < chosen_author_num and epoch < max_epoch:
        # print(epoch, len(chosen_paper), len(chosen_author))
        epoch += 1
        curpaperid = random_walk_according_to_time(
            board_to_pin, userid, cache_user_candidates, current_date)
        while True:
            curuserid = random_walk_according_to_time(
                pin_to_board, curpaperid, cache_paper_candidates, current_date)
            if curuserid != userid:
                if curuserid in count_author:
                    count_author[curuserid] += 1
                    if count_author[curuserid] >= threshold_author:
                        chosen_author.add(curuserid)
                else:
                    count_author[curuserid] = 1
            curpaperid = random_walk_according_to_time(
                board_to_pin, curuserid, cache_user_candidates, current_date)
            if random.random() < alpha:
                break

    return sorted(
        [(authorid, count_author[authorid]) for authorid in chosen_author],
        key=lambda x: x[1], reverse=True
    )


if __name__ == "__main__":

    userNum = 80000
    paperNum = 2000000

    print("[INFO] Generate Data...")
    board_to_pin = generate_board_to_pin(userNum, paperNum)
    pin_to_board = generate_pin_to_board(board_to_pin)

    cache_user_candidates = dict()
    cache_paper_candidates = dict()

    print("[INFO] Start Running...")
    time_start = time.time()

    # for userid in tqdm(range(userNum)):
    #     chosen = pixie_random_walk(userid, 30, 50)

    for userid in tqdm(range(userNum)):

        # time_start = time.time()

        # chosen_paper, chosen_author = pixie_random_walk(board_to_pin, pin_to_board, cache_user_candidates, cache_paper_candidates, userid, 30, 50, 60)
        # chosen_paper = pixie_random_walk_only_paper(board_to_pin, pin_to_board, cache_user_candidates, cache_paper_candidates, userid, 20, 60)
        chosen_author = pixie_random_walk_only_author(
            board_to_pin, pin_to_board, cache_user_candidates,
            cache_paper_candidates, userid, 20, 60
        )
        # print(chosen_paper)

        # time_end = time.time()

        # print(time_end - time_start)

    # for paper in chosen_paper:
    #     print(paper)
    # print("-----------------------------------------")
    # for author in chosen_author:
    #     print(author)
