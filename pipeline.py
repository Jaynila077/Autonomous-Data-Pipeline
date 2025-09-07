from memory import Memory
from agents import parser, fetcher, cleaner, analyzer, reporter, profiler, analysis_strategy, cleaning_strategy, feature_engineering, vector_store_agent
from utils.logger import logger
import pandas as pd
import os
from rq import get_current_job

def run_pipeline(job, file_path: str, goal: str):
   
    job = get_current_job()
    logger.info(f"Starting pipeline for file: {file_path}")
    
    try:
        file_name = os.path.basename(file_path)
        user_request = f"Analyze the data in the file named '{file_name}'. The user's main goal is: '{goal}'"

       
        job.meta['status'] = 'Parsing request...'
        job.save_meta()
        memory = Memory()
        parsed = parser.parse(user_request)
        parsed["file_path"] = file_path
        memory.set("parsed", parsed)

   
        job.meta['status'] = 'Profiling data...'
        job.save_meta()
        df = fetcher.fetch(parsed["file_path"])
        memory.set("raw_df", df)
        profile = profiler.profile(df)
        memory.set("profile", profile)
        
        job.meta['status'] = 'Generating analysis plans...'
        job.save_meta()
        clean_plan = cleaning_strategy.get_cleaning_plan(profile)
        analysis_plan = analysis_strategy.get_analysis_plan(profile)
        memory.set("cleaning_plan", clean_plan)
        memory.set("analysis_plan", analysis_plan)
  
        job.meta['status'] = 'Cleaning data and engineering features...'
        job.save_meta()
        df_clean = cleaner.clean(df.copy(), clean_plan)
        memory.set("clean_df", df_clean)
        df_featured = feature_engineering.engineer_features(df_clean.copy(), analysis_plan)
        memory.set("featured_df", df_featured)

        job.meta['status'] = 'Running analysis...'
        job.save_meta()
        stats = analyzer.analyze(df_featured.copy(), analysis_plan)
        memory.set("stats", stats)

        job.meta['status'] = 'Generating report...'
        job.save_meta()
        reporter.write_report(stats)
        
        job.meta['status'] = 'Storing data in vector DB...'
        job.save_meta()
        vector_store_agent.store_data(df_clean)
        
        logger.info(f"Pipeline finished for file: {file_path}")
        output_files = [f for f in os.listdir('output') if os.path.isfile(os.path.join('output', f))]

        job.meta['status'] = 'Complete'
        job.save_meta()
        return {"status": "Complete", "summary_stats": stats, "output_files": output_files}

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        job.meta['status'] = 'Failed'
        job.meta['error'] = str(e)
        job.save_meta()
        raise e