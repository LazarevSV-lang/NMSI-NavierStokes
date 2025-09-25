# Taylor–Green Sweep Notebook
# Runs 128² and 256² tests and plots E(t), Ω(t), max|ω|

import subprocess

def run_case(nx, nu, t_end, aug):
    args = ["python", "tg_benchmark.py",
            "--nx", str(nx), "--ny", str(nx),
            "--nu", str(nu), "--t_end", str(t_end)]
    if aug:
        args += ["--aug", "on"]
    else:
        args += ["--aug", "off"]
    subprocess.run(args)

print("Running 128² classical & augmented...")
run_case(128, 5e-4, 6, False)
run_case(128, 5e-4, 6, True)

print("Running 256² classical & augmented...")
run_case(256, 2e-4, 8, False)
run_case(256, 2e-4, 8, True)

print("Use plot_results.py to visualize outputs.")
