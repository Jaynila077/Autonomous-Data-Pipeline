from memory import Memory
from agents import parser, fetcher, cleaner, analyzer, reporter , profiler , analysis_strategy , cleaning_strategy

def run_pipeline(user_input):
    print("Starting pipeline...")
    memory = Memory()

    parsed = parser.parse(user_input)
    print("Parsed:", parsed)
    memory.set("parsed", parsed)

    df = fetcher.fetch(parsed["file_path"])
    print("Data fetched")
    memory.set("raw_df", df)

    profile = profiler.profile(df)
    memory.set("profile", profile)
    
    clean_plan = cleaning_strategy.get_cleaning_plan(profile)
    memory.set("cleaning_plan", clean_plan)

    analysis_plan = analysis_strategy.get_analysis_plan(profile)
    memory.set("analysis_plan", analysis_plan)

    df_clean = cleaner.clean(df, clean_plan)
    print("Data cleaned")
    memory.set("clean_df", df_clean)

    stats = analyzer.analyze(df, analysis_plan)
    print("Analysis complete:", stats)
    memory.set("stats", stats)

    reporter.write_report(stats)
    print("Report written to `output/report.md`")


if __name__ == "__main__":
    user_request = "Analyze rainfall patterns in the file data/sample.csv focusing on Rainfall column"
    run_pipeline(user_request)

