from datetime import date, timedelta

# Inputs
principal = 352559.19  # Balance as of Jan 14
annual_rate = 0.0488  # 4.88%
payment = 494.23
maturity_date = date(2026, 4, 1)
next_pmt_date = date(2026, 1, 15)

# 1. Canadian Mortgage Math (Semi-annual compounding)
# Weekly rate formula: (1 + r/2)^(2/52) - 1
weekly_rate = (1 + annual_rate / 2) ** (2 / 52) - 1
# Daily rate for the final stub period: (1 + r/2)^(2/365) - 1
daily_rate = (1 + annual_rate / 2) ** (2 / 365) - 1

current_date = next_pmt_date

# 2. Process all weekly payments until maturity
while current_date <= maturity_date:
    # Interest for the week is calculated on the current principal
    interest_charge = principal * weekly_rate

    # Principal reduction is the payment minus the interest
    principal_reduction = payment - interest_charge
    principal -= principal_reduction

    last_pmt_date = current_date
    current_date += timedelta(days=7)

# 3. Handle the 'Stub Period' (Interest accrued after the last payment)
days_since_last_pmt = (maturity_date - last_pmt_date).days
accrued_interest = principal * ((1 + daily_rate) ** days_since_last_pmt - 1)

final_payout = principal + accrued_interest

print(f"Principal after last payment (Mar 26): ${principal:,.2f}")
print(f"Accrued interest (6 days till maturity): ${accrued_interest:,.2f}")
print(f"Balance at Maturity (Apr 1): ${final_payout:,.2f}")