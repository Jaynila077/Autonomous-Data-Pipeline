def write_report(stats):
    print("[Reporter] Writing report...")
    with open("output/report.md", "w") as f:
        f.write("# Auto Report\n\n")
        f.write("## Statistics\n")
        for k, v in stats.items():
            f.write(f"- **{k}**: {v}\n")
        f.write("\n\n![Chart](chart.png)")
