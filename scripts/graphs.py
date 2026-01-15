import matplotlib.pyplot as plt

from parse_yaml import load_matches, ensure_data_present

def compute_data(match):
    """Compute outcome tallies for both innings in a match."""

    outcomes = {
        "1st innings": {},
        "2nd innings": {}
    }

    innings_lst = [["1st innings", 0], ["2nd innings", 1]]
    
    for innings_name, idx in innings_lst:
        if idx >= len(match["innings"]):
            continue

        for delivery in match["innings"][idx][innings_name]["deliveries"]:
            outcome = extract_outcome(delivery)
            if outcome in outcomes[innings_name]:
                outcomes[innings_name][outcome] += 1
            else:
                outcomes[innings_name][outcome] = 1

    return outcomes


def extract_outcome(delivery_obj):
    _, delivery = next(iter(delivery_obj.items()))

    # Wicket takes priority
    if "wicket" in delivery:
        return "W"

    # Otherwise return total runs
    return delivery["runs"]["total"]


def merge_tallies(global_tally, match_tally):
    """Merge match tallies into global tallies."""
    for innings in ["1st innings", "2nd innings"]:
        if innings not in global_tally:
            global_tally[innings] = {}
        for total, count in match_tally[innings].items():
            global_tally[innings][total] = global_tally[innings].get(total, 0) + count
    return global_tally


def calc_percentages(tallies):
    """Convert tallies to percentages for each innings."""
    percentages_dict = {}
    for innings, counts in tallies.items():
        total_deliveries = sum(counts.values())
        outcomes = sorted(
            counts.keys(),
            key=lambda x: (x == "W", x if isinstance(x, int) else 0)
        )
        percentages = [counts[o] / total_deliveries * 100 for o in outcomes]
        percentages_dict[innings] = {"outcomes": outcomes, "percentages": percentages}
    return percentages_dict

def plot_innings_percentages(percentages_dict):
    """Plot both innings on one figure using subplots."""
    innings_list = list(percentages_dict.keys())
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)  

    for ax, innings in zip(axes, innings_list):
        data = percentages_dict[innings]
        outcomes = data["outcomes"]
        percentages = data["percentages"]

        ax.bar([str(o) for o in outcomes], percentages, color='skyblue')
        ax.set_title(f'{innings}')
        ax.set_xlabel('Runs / Outcome')
        ax.set_ylabel('Percentage (%)')
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.suptitle('Percentage of Each Outcome per Ball')
    plt.tight_layout(rect=[0, 0, 1, 0.95])  
    plt.show()

def produce_statistics():
    """Produce and plot statistics from all matches."""
    ensure_data_present()
    global_tally = {"1st innings": {}, "2nd innings": {}}
    for match_id, match in load_matches():
        match_outcomes = compute_data(match)
        global_tally = merge_tallies(global_tally, match_outcomes)
    
    percentages_dict = calc_percentages(global_tally)
    plot_innings_percentages(percentages_dict)
    print(percentages_dict)
    return percentages_dict
 

if __name__ == "__main__":
    ensure_data_present()
    produce_statistics()