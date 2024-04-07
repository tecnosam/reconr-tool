from typing import List
import typer

from reconr import (
    read_csv,
    find_missing_records,
    find_discrapancies,
    write_to_csv
)


app = typer.Typer()


@app.command()
def main(
    source_fn: str,
    target_fn: str,
    output_fn: str = 'reconcilation.csv',
    is_case_sensitive: bool = False,
    headers: List[str] = None,
    use_fuzzy: bool = False,
    threshold: int = 90
):

    source = read_csv(source_fn, is_case_sensitive, headers)
    target = read_csv(target_fn, is_case_sensitive, headers)

    if source is None or target is None:

        print("Exiting...")
        return

    missing_records = find_missing_records(source, target)

    discrapancies = find_discrapancies(
        source,
        target,
        use_fuzzy,
        threshold
    )

    write_to_csv(output_fn, missing_records, discrapancies)

    print("Reconciliation completed:")

    print(f"- Records missing in target: {len(missing_records[1])}")
    print(f"- Records missing in source: {len(missing_records[0])}")
    print(f"- Records with field discrapancies: {len(discrapancies)}")

    print(f"\nReport saved to: {output_fn}")


app()
