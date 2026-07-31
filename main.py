
import csv
import sys


def load_stock(filepath):
    """Read the stock CSV into a list of dictionaries."""
    stock_items = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                stock_items.append({
                    "item_name": row["item_name"].strip(),
                    "current_quantity": int(row["current_quantity"]),
                    "reorder_threshold": int(row["reorder_threshold"]),
                })
            except (ValueError, KeyError) as e:
                # Skip malformed rows instead of crashing the whole run
                print(f"Skipping bad row {row}: {e}")
    return stock_items


def classify_priority(current_quantity, reorder_threshold):
    """Return 'Critical' if qty is below 25% of threshold, else 'Low'."""
    critical_cutoff = reorder_threshold * 0.25
    if current_quantity < critical_cutoff:
        return "Critical"
    return "Low"


def find_low_stock(stock_items):
    """Compare each item's quantity against its threshold, flag + tag priority."""
    low_stock = []
    for item in stock_items:
        if item["current_quantity"] < item["reorder_threshold"]:
            item["priority"] = classify_priority(
                item["current_quantity"], item["reorder_threshold"]
            )
            low_stock.append(item)
    return low_stock


def print_report(low_stock_items):
    """Print a clean restock-needed report to the console."""
    if not low_stock_items:
        print("All items are sufficiently stocked. No reorder needed.")
        return

    print("RESTOCK NEEDED REPORT")
    print("-" * 55)
    print(f"{'Item':<25}{'Qty':<8}{'Threshold':<10}{'Priority':<10}")
    print("-" * 55)
    for item in low_stock_items:
        print(f"{item['item_name']:<25}{item['current_quantity']:<8}"
              f"{item['reorder_threshold']:<10}{item['priority']:<10}")
    print("-" * 55)
    print(f"Total items needing reorder: {len(low_stock_items)}")


def write_report_csv(low_stock_items, out_path="restock_report.csv"):
    """Write the flagged items out to a CSV report."""
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["item_name", "current_quantity", "reorder_threshold", "priority"]
        )
        writer.writeheader()
        writer.writerows(low_stock_items)
    print(f"Report written to {out_path}")


def send_email_alert(low_stock_items):
    """
    Simulated email alert (no real email is sent).
    In a production system, this is where an SMTP/email API call
    (e.g. smtplib, SendGrid, SES) would go.
    """
    critical_items = [i for i in low_stock_items if i["priority"] == "Critical"]
    if not critical_items:
        print("\n[EMAIL ALERT] No critical items — no alert email needed.")
        return

    print("\n[EMAIL ALERT - SIMULATED]")
    print("To: warehouse-manager@company.com")
    print("Subject: URGENT - Critical Stock Levels Detected")
    print("Body:")
    print("  The following items are critically low and need immediate reorder:")
    for item in critical_items:
        print(f"   - {item['item_name']} (Qty: {item['current_quantity']}, "
              f"Threshold: {item['reorder_threshold']})")
    print("[EMAIL ALERT] Simulated send complete.\n")


def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else "stock.csv"

    stock_items = load_stock(filepath)
    low_stock_items = find_low_stock(stock_items)

    print_report(low_stock_items)

    if low_stock_items:
        write_report_csv(low_stock_items)
        send_email_alert(low_stock_items)


if __name__ == "__main__":
    main()


