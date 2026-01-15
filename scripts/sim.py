from graphs import produce_statistics
import random


def sim(number_of_balls=120):
    """Simulate a match using computed probabilities."""
    runs = [0, 0]
    wickets = [0, 0]
    # probabilities = produce_statistics()
    probabilities = {'1st innings': {'outcomes': [0, 1, 2, 3, 4, 5, 6, 7, 'W'], 'percentages': [35.145020640954186, 38.679679756513494, 7.779320333592528, 0.6020417357757628, 9.027121913451493, 0.21675504844033147, 2.9793390222495137, 0.023694547250598202, 5.5470270017720855]}, '2nd innings': {'outcomes': [0, 1, 2, 3, 4, 5, 6, 7, 8, 'W'], 'percentages': [37.52718545619692, 37.60215956761667, 6.85279038765335, 0.5120947140315126, 8.95695937890898, 0.2067171322696014, 2.770910044769136, 0.013702840207265246, 0.00019575486010378924, 5.557284723486473]}}
    innings_names = ["1st innings", "2nd innings"]

    for i in range(2):
        innings_key = innings_names[i]

        for ball in range(number_of_balls):
            rand = random.random() * 100
            cumulative = 0

            for outcome, prob in zip(
                probabilities[innings_key]["outcomes"],
                probabilities[innings_key]["percentages"]
            ):
                if outcome == "W":
                    if wickets[i] == 10:
                        continue
                    wickets[i] += 1
                else:
                    cumulative += prob
                    if rand <= cumulative:
                        runs[i] += outcome
                        break
                    if runs[1] > runs[0]:
                        return runs[0], wickets[0], runs[1], wickets[1]
    
    return runs[0], wickets[0], runs[1], wickets[1]

if __name__ == "__main__":
    runs1, wickets1, runs2, wickets2 = sim()
    print(f"1st Innings: {runs1}/{wickets1}")
    print(f"2nd Innings: {runs2}/{wickets2}")
    if runs1 > runs2:
        print("1st Innings Win")
    elif runs2 > runs1:
        print("2nd Innings Win")
    else:
        print("Draw")