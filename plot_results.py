
import argparse, numpy as np
import matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--classical", type=str, default=None, help="Path to tg_classical_timeseries.npz")
    ap.add_argument("--augmented", type=str, default=None, help="Path to tg_aug_timeseries.npz")
    ap.add_argument("--out", type=str, default="out_plots")
    args = ap.parse_args()

    import os; os.makedirs(args.out, exist_ok=True)

    if args.classical:
        C = np.load(args.classical, allow_pickle=True)
    if args.augmented:
        A = np.load(args.augmented, allow_pickle=True)

    def plot_series(key, ylabel, fname):
        plt.figure()
        if args.classical:
            plt.plot(C["t"], C[key], "--", label="Classical NSE")
        if args.augmented:
            plt.plot(A["t"], A[key], label="NMSI π*+γ_diss+e*")
        plt.xlabel("t"); plt.ylabel(ylabel); plt.legend(); plt.tight_layout()
        plt.savefig(fname); plt.close()

    if args.classical or args.augmented:
        plot_series("E",  "Energy E(t)",      f"{args.out}/E_t.png")
        plot_series("Om", "Enstrophy Ω(t)",   f"{args.out}/Omega_t.png")
        plot_series("W",  "max|ω|",           f"{args.out}/wmax_t.png")

    print("Saved plots to", args.out)

if __name__ == "__main__":
    main()
