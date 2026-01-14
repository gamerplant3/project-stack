import pandas as pd

# --- Mortgage Parameters ---
principal = 350989.65
annual_rate = 0.0369
years = 25
term_years = 5

# --- Canadian Interest Compounding Math ---
# Interest in Canada is compounded semi-annually
i_sa = annual_rate / 2
i_m = (1 + i_sa) ** (2 / 12) - 1  # Effective Monthly Rate
i_w = (1 + i_sa) ** (2 / 52) - 1  # Effective Weekly Rate

# --- Base Payment Calculations ---
monthly_pmt = round(principal * (i_m / (1 - (1 + i_m) ** (-years * 12))), 2)
acc_weekly_pmt = round(monthly_pmt / 4, 2)

def calculate_term_stats(base_pmt, weekly_extra, frequency='weekly'):
    balance = principal
    total_interest = 0
    total_principal_paid = 0

    if frequency == 'monthly':
        # month-by-month for 60 months
        for m in range(term_years * 12):
            interest_charge = balance * i_m
            # weekly extra is converted to monthly equivalent (Weekly * 52 / 12)
            extra = weekly_extra * (52 / 12)
            principal_reduction = (base_pmt - interest_charge) + extra
            balance -= principal_reduction
            total_interest += interest_charge
            total_principal_paid += principal_reduction
    else:
        # week-by-week for 260 weeks
        for w in range(term_years * 52):
            interest_charge = balance * i_w
            principal_reduction = (base_pmt + weekly_extra) - interest_charge
            balance -= principal_reduction
            total_interest += interest_charge
            total_principal_paid += principal_reduction

    return round(total_principal_paid, 2), round(total_interest, 2), round(balance, 2)

# --- Analysis of different scenarios ---
extras = [0, 100, 150, 200, 250]

# 1. Baseline Monthly Interest (The "Do Nothing" interest cost)
baseline_int_m = calculate_term_stats(monthly_pmt, 0, 'monthly')[1]

# 2. Baseline Accelerated Weekly Interest (To isolate frequency savings)
baseline_int_acc_only = calculate_term_stats(acc_weekly_pmt, 0, 'weekly')[1]
saved_by_freq = round(baseline_int_m - baseline_int_acc_only, 2)

# --- Table 1: Monthly ---
monthly_rows = []
for e in extras:
    total_principal, total_interest, bal = calculate_term_stats(monthly_pmt, e, 'monthly')
    int_saved = round(baseline_int_m - total_interest, 2)
    monthly_rows.append([f"${e}", "Weekly", f"${e * 52 * 5:,.2f}", f"${total_principal:,.2f}", f"${int_saved:,.2f}", f"${bal:,.2f}"])

# 2. Accelerated Weekly Payments Table
acc_rows = []
for e in extras:
    total_principal, total_interest, bal = calculate_term_stats(acc_weekly_pmt, e, 'weekly')
    total_int_saved = round(baseline_int_m - total_interest, 2)
    saved_by_prepay = round(baseline_int_acc_only - total_interest, 2)

    acc_rows.append([
        f"${e}",
        "Weekly",
        f"${e * 52 * term_years:,.2f}",
        f"${total_principal:,.2f}",
        f"${saved_by_freq:,.2f}",
        f"${saved_by_prepay:,.2f}",
        f"${total_int_saved:,.2f}",
        f"${bal:,.2f}"
    ])

# Displaying results
cols_m = ["Extra", "Freq", "Prepayments", "Principal Paid", "Interest Saved", "Balance at Renewal"]
cols_a = ["Extra", "Freq", "Prepayments", "Principal Paid", "Saved by Freq", "Saved by Prepay", "Total Int Saved", "Balance at Renewal"]
df_m = pd.DataFrame(monthly_rows, columns=cols_m)
df_a = pd.DataFrame(acc_rows, columns=cols_a)

print(f"--- TABLE 1: MONTHLY PAYMENTS OVER {term_years} YRS (${monthly_pmt:,.2f}) ---")
print(df_m.to_string(index=False))
print(f"\n--- TABLE 2: ACCELERATED WEEKLY PAYMENTS OVER {term_years} YRS (${acc_weekly_pmt:,.2f}) ---")
print(df_a.to_string(index=False))