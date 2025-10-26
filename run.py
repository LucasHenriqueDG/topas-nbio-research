import subprocess
import time
import Utils as utils

simulations = utils.read_param_file("params")

cur_seed = 0
successful_simulations = 0
tries = 0
for name, params in simulations.items():
    seeds = params["seeds"]
    energy = params["energy"]
    particle = params["particle"]

    print(f"Starting simulation for scenario {name}")
    time.sleep(1)

    #Execute the simulation
    while successful_simulations < seeds:

        simulation_params = {"seeds": cur_seed, "energy": energy, "particle": particle, "histories": params["histories"]}

        utils.update_parameters(simulation_params)

        folder_name = f"{name}_{energy}_{particle}"
        tgt_dir = "outputs"

        tries += 1
        print(f"Starting simulation for seed {cur_seed}. Trying for the {tries}° seed...")
        time.sleep(5)
        cmd = "~/Applications/TOPAS/OpenTOPAS-install/bin/topas run.txt"
        process = subprocess.Popen(cmd, shell=True)
        process.wait()

        time.sleep(1)

        print("Simulation finished. Checking if there were any crashes...")
        outcome = utils.check_simulation()
        if outcome:
            print("Simulation was successful. Moving files...")
            time.sleep(2)
            include_list = [
                "DNADamage.phsp",
                "DNADamage.header",
                "DNADamage_full.csv",
                "DNADamage_sdd.txt"
            ]
            utils.move_files(folder_name, "", include_list=include_list, tgt_dir=tgt_dir)
            successful_simulations += 1

            if cur_seed >= seeds:
                break
        else:
            print("Simulation crashed. Starting a new seed...")
            utils.save_problematic_seed(cur_seed, particle)
            time.sleep(1)

        cur_seed += 1

    print(f"Finishing simulations for {name}")
    print(f"Total amount of tries: {tries}")
    print(f"Total amount of successful simulations: {successful_simulations}")
    successful_simulations = 0
    cur_seed = 0
    tries = 0

print("All the simulations were finished.")
