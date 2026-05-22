import io
import linecache
import pathlib
import sys
import trace
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tss_project" / "shopping_cart.py"
sys.path.insert(0, str(ROOT))


def executable_lines(path):
    prefixes = ("if ", "raise ", "return ", "total =", "subtotal =", "taxable_amount =", "final_total =")
    lines = []
    for number, text in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = text.strip()
        is_function_body = text.startswith("        ")
        is_code = stripped.startswith(prefixes)
        if is_function_body and is_code:
            lines.append(number)
    return set(lines)


def main():
    tracer = trace.Trace(count=True, trace=False)
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    output = io.StringIO()
    runner = unittest.TextTestRunner(stream=output, verbosity=2)
    result = tracer.runfunc(runner.run, suite)

    counts = tracer.results().counts
    covered = {
        line
        for (filename, line), count in counts.items()
        if pathlib.Path(filename).resolve() == SOURCE.resolve() and count > 0
    }
    executable = executable_lines(SOURCE)
    missing = sorted(executable - covered)
    coverage = 100.0 if not executable else len(covered & executable) / len(executable) * 100

    print("Unit test result:", "OK" if result.wasSuccessful() else "FAILED")
    print(f"Statement coverage for {SOURCE.name}: {coverage:.2f}%")
    print(f"Covered executable lines: {len(covered & executable)}/{len(executable)}")
    print("Missing executable lines:", missing if missing else "none")

    if not result.wasSuccessful():
        print(output.getvalue())
        raise SystemExit(1)


if __name__ == "__main__":
    linecache.clearcache()
    main()
