from memory import Memory
from agents import parser, fetcher, cleaner, analyzer, reporter , profiler , analysis_strategy , cleaning_strategy
from utils.logger import logger


def run_pipeline(user_input):
    logger.info("Starting pipeline...")
    memory = Memory()

    parsed = parser.parse(user_input)
    logger.info("Parsed:", parsed)
    memory.set("parsed", parsed)

    df = fetcher.fetch(parsed["file_path"])
    logger.info("Data fetched")
    memory.set("raw_df", df)

    profile = profiler.profile(df)
    logger.info("Profile complete:", profile)
    memory.set("profile", profile)
    
    clean_plan = cleaning_strategy.get_cleaning_plan(profile)
    logger.info("Cleaning plan complete:", clean_plan)
    memory.set("cleaning_plan", clean_plan)

    analysis_plan = analysis_strategy.get_analysis_plan(profile)
    logger.info("Analysis plan complete:", analysis_plan)
    memory.set("analysis_plan", analysis_plan)

    df_clean = cleaner.clean(df, clean_plan)
    logger.info("Data cleaned")
    memory.set("clean_df", df_clean)

    stats = analyzer.analyze(df, analysis_plan)
    logger.info("Analysis complete:", stats)
    memory.set("stats", stats)

    reporter.write_report(stats)
    logger.info("Report written to `output/report.md`")




if __name__ == "__main__":
    user_request = "Analyze rainfall patterns in the file data/sample.csv focusing on Rainfall column"
    run_pipeline(user_request)

