from memory import Memory
from agents import parser, fetcher, cleaner, analyzer, reporter

def run_pipeline(user_input):
    print("Starting pipeline...")
    memory = Memory()

    parsed = parser.parse(user_input)
    print("Parsed:", parsed)
    memory.set("parsed", parsed)

    df = fetcher.fetch(parsed["file_path"])
    print("Data fetched")
    memory.set("raw_df", df)

    df_clean = cleaner.clean(df)
    print("Data cleaned")
    memory.set("clean_df", df_clean)

    stats = analyzer.analyze(df_clean, parsed["target_column"])
    print("Analysis complete:", stats)
    memory.set("stats", stats)

    reporter.write_report(stats)
    print("Report written to `output/report.md`")


if __name__ == "__main__":
    user_request = "Analyze rainfall patterns in the file data/sample.csv focusing on Rainfall column"
    run_pipeline(user_request)

