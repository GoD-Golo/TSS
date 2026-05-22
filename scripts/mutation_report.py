import argparse
import pathlib
import shutil
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]

MUTATIONS = [
    ("M01_vat_19_to_20", "VAT_RATE = 0.19", "VAT_RATE = 0.20"),
    ("M02_discount_threshold_500_to_600", "DISCOUNT_THRESHOLD = 500.0", "DISCOUNT_THRESHOLD = 600.0"),
    ("M03_discount_rate_10_to_5", "DISCOUNT_RATE = 0.10", "DISCOUNT_RATE = 0.05"),
    ("M04_free_shipping_300_to_400", "FREE_SHIPPING_THRESHOLD = 300.0", "FREE_SHIPPING_THRESHOLD = 400.0"),
    ("M05_standard_shipping_20_to_10", "STANDARD_SHIPPING = 20.0", "STANDARD_SHIPPING = 10.0"),
    ("M06_discount_boundary_ge_to_gt", "if subtotal >= self.DISCOUNT_THRESHOLD:", "if subtotal > self.DISCOUNT_THRESHOLD:"),
    ("M07_shipping_boundary_ge_to_gt", "if subtotal_after_discount >= self.FREE_SHIPPING_THRESHOLD:", "if subtotal_after_discount > self.FREE_SHIPPING_THRESHOLD:"),
    ("M08_allow_zero_price", "if unit_price <= 0:", "if unit_price < 0:"),
    ("M09_remove_name_trim", "self._items.append(CartItem(name.strip(), unit_price, quantity))", "self._items.append(CartItem(name, unit_price, quantity))"),
    ("M10_classification_boundary_300_to_301", "if subtotal < self.FREE_SHIPPING_THRESHOLD:", "if subtotal <= self.FREE_SHIPPING_THRESHOLD:"),
]


def copy_project(destination):
    for name in ["tss_project", "tests"]:
        shutil.copytree(ROOT / name, destination / name)


def mutate_source(destination, search, replacement):
    target = destination / "tss_project" / "shopping_cart.py"
    text = target.read_text(encoding="utf-8")
    if search not in text:
        raise RuntimeError(f"Mutation pattern not found: {search}")
    target.write_text(text.replace(search, replacement, 1), encoding="utf-8")


def run_suite(destination, pattern):
    command = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-p",
        pattern,
    ]
    return subprocess.run(command, cwd=destination, text=True, capture_output=True)


def analyze(pattern):
    rows = []
    suite_name = "base" if pattern == "test_shopping_cart_base.py" else "full"
    for mutant_id, search, replacement in MUTATIONS:
        tmp = ROOT / ".mutation_tmp" / suite_name / mutant_id
        if tmp.exists():
            shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir(parents=True)
        try:
            copy_project(tmp)
            mutate_source(tmp, search, replacement)
            completed = run_suite(tmp, pattern)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        status = "KILLED" if completed.returncode != 0 else "SURVIVED"
        rows.append((mutant_id, status, search, replacement))
    return rows


def print_table(title, rows):
    print(f"\n## {title}")
    print("| Mutant | Status | Original | Mutatie |")
    print("|---|---:|---|---|")
    for mutant_id, status, search, replacement in rows:
        print(f"| {mutant_id} | {status} | `{search}` | `{replacement}` |")
    killed = sum(1 for _, status, _, _ in rows if status == "KILLED")
    print(f"\nMutation score: {killed}/{len(rows)} = {killed / len(rows) * 100:.2f}%")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--suite",
        choices=["base", "full"],
        default="full",
        help="base runs only the initial suite; full runs every test file",
    )
    args = parser.parse_args()
    pattern = "test_shopping_cart_base.py" if args.suite == "base" else "test_*.py"
    rows = analyze(pattern)
    print_table(f"Mutation report for {args.suite} suite", rows)


if __name__ == "__main__":
    main()
