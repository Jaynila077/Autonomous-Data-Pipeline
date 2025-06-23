from memory import Memory
from agents import parser, fetcher, cleaner, analyzer, reporter

def run_pipeline(user_input):
    memory = Memory()

    parsed = parser.parse(user_input)
    memory.set("parsed", parsed)

    df = fetcher.fetch(parsed["file_path"])
    memory.set("raw_df", df)

    df_clean = cleaner.clean(df)
    memory.set("clean_df", df_clean)

    stats = analyzer.analyze(df_clean, parsed["target_column"])
    memory.set("stats", stats)

    reporter.write_report(stats)
    print("\n✅ Pipeline completed. Check the 'output/' folder.")

if __name__ == "__main__":
    user_request = "Analyze rainfall trend using the CSV file"
    run_pipeline(user_request)
